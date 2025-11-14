"""
Scraper Manager
Coordinates multiple rental listing scrapers, runs them in parallel,
aggregates results, and handles deduplication.
"""

import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from difflib import SequenceMatcher
from typing import Any, Dict, List, Optional, Set

from scrapers.kijiji_scraper import KijijiScraper
from scrapers.realtor_ca_scraper import RealtorCAScraper
from scrapers.rentals_ca_scraper import RentalsCAScraper


class ScraperManager:
    """
    Manages multiple scrapers, coordinates execution, and aggregates results.
    """

    # Available scrapers registry
    AVAILABLE_SCRAPERS = {
        "kijiji": KijijiScraper,
        "realtor_ca": RealtorCAScraper,
        "rentals_ca": RentalsCAScraper,
        # Future scrapers will be added here
        # "viewit_ca": ViewitCAScraper,
        # "apartments_ca": ApartmentsCAScraper,
    }

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the scraper manager.

        Args:
            config: Configuration dictionary with options:
                - enabled_scrapers: List of scraper names to use (default: all)
                - max_workers: Max parallel scrapers (default: 3)
                - timeout: Overall timeout in seconds (default: 60)
                - deduplicate: Enable deduplication (default: True)
                - similarity_threshold: Deduplication threshold 0-1 (default: 0.85)
                - scraper_configs: Dict of per-scraper configs
        """
        self.config = config or {}
        self.logger = logging.getLogger(__name__)

        # Get enabled scrapers (default: all available)
        enabled = self.config.get(
            "enabled_scrapers", list(self.AVAILABLE_SCRAPERS.keys())
        )

        # Filter to only valid scrapers
        self.enabled_scrapers = [
            name for name in enabled if name in self.AVAILABLE_SCRAPERS
        ]

        if not self.enabled_scrapers:
            self.logger.warning("No scrapers enabled, using all available scrapers")
            self.enabled_scrapers = list(self.AVAILABLE_SCRAPERS.keys())

        self.logger.info(f"Enabled scrapers: {', '.join(self.enabled_scrapers)}")

        # Configuration
        self.max_workers = self.config.get("max_workers", 3)
        self.timeout = self.config.get("timeout", 60)
        self.deduplicate = self.config.get("deduplicate", True)
        self.similarity_threshold = self.config.get("similarity_threshold", 0.85)

        # Per-scraper configurations
        self.scraper_configs = self.config.get("scraper_configs", {})

        # Statistics
        self.stats = {
            "total_listings": 0,
            "unique_listings": 0,
            "duplicates_removed": 0,
            "scrapers_succeeded": 0,
            "scrapers_failed": 0,
            "execution_time": 0,
            "by_source": {},
        }

    def search_all(
        self,
        location: str,
        min_price: Optional[int] = None,
        max_price: Optional[int] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Search all enabled scrapers in parallel and aggregate results.

        Args:
            location: Location/city to search
            min_price: Minimum price filter
            max_price: Maximum price filter
            **kwargs: Additional search parameters

        Returns:
            Dictionary containing:
                - listings: List of aggregated listings
                - stats: Statistics about the search
                - errors: Any errors encountered
        """
        start_time = time.time()

        self.logger.info(
            f"Starting multi-source search - "
            f"Location: {location}, Price: ${min_price}-${max_price}"
        )
        self.logger.info(f"Using {len(self.enabled_scrapers)} scrapers in parallel")

        # Results containers
        all_listings = []
        errors = {}

        # Run scrapers in parallel
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all scraper tasks
            future_to_scraper = {}

            for scraper_name in self.enabled_scrapers:
                future = executor.submit(
                    self._run_scraper,
                    scraper_name,
                    location,
                    min_price,
                    max_price,
                    **kwargs,
                )
                future_to_scraper[future] = scraper_name

            # Collect results as they complete
            for future in as_completed(future_to_scraper, timeout=self.timeout):
                scraper_name = future_to_scraper[future]

                try:
                    result = future.result()

                    if result["success"]:
                        listings = result["listings"]
                        all_listings.extend(listings)

                        self.stats["scrapers_succeeded"] += 1
                        self.stats["by_source"][scraper_name] = len(listings)

                        self.logger.info(
                            f"✓ {scraper_name}: {len(listings)} listings "
                            f"({result['execution_time']:.2f}s)"
                        )
                    else:
                        self.stats["scrapers_failed"] += 1
                        errors[scraper_name] = result["error"]

                        self.logger.warning(
                            f"✗ {scraper_name} failed: {result['error']}"
                        )

                except Exception as e:
                    self.stats["scrapers_failed"] += 1
                    errors[scraper_name] = str(e)
                    self.logger.error(f"✗ {scraper_name} exception: {e}")

        # Update statistics
        self.stats["total_listings"] = len(all_listings)

        # Deduplicate if enabled
        if self.deduplicate and len(all_listings) > 1:
            self.logger.info("Deduplicating listings...")
            unique_listings = self._deduplicate_listings(all_listings)
            self.stats["unique_listings"] = len(unique_listings)
            self.stats["duplicates_removed"] = len(all_listings) - len(unique_listings)
            self.logger.info(
                f"Removed {self.stats['duplicates_removed']} duplicates, "
                f"{self.stats['unique_listings']} unique listings remaining"
            )
        else:
            unique_listings = all_listings
            self.stats["unique_listings"] = len(unique_listings)
            self.stats["duplicates_removed"] = 0

        # Calculate execution time
        self.stats["execution_time"] = time.time() - start_time

        # Sort by price (ascending)
        unique_listings.sort(key=lambda x: x.get("price") or float("inf"))

        # Build response
        response = {
            "listings": unique_listings,
            "stats": self.stats.copy(),
            "errors": errors,
            "search_params": {
                "location": location,
                "min_price": min_price,
                "max_price": max_price,
            },
            "timestamp": datetime.utcnow().isoformat(),
        }

        self.logger.info(
            f"Search complete: {self.stats['unique_listings']} unique listings "
            f"from {self.stats['scrapers_succeeded']} sources "
            f"in {self.stats['execution_time']:.2f}s"
        )

        return response

    def _run_scraper(
        self,
        scraper_name: str,
        location: str,
        min_price: Optional[int],
        max_price: Optional[int],
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Run a single scraper and return results.

        Args:
            scraper_name: Name of the scraper to run
            location: Location to search
            min_price: Minimum price
            max_price: Maximum price
            **kwargs: Additional parameters

        Returns:
            Dictionary with success status, listings, and execution time
        """
        start_time = time.time()

        try:
            # Get scraper class
            scraper_class = self.AVAILABLE_SCRAPERS[scraper_name]

            # Get scraper-specific config
            scraper_config = self.scraper_configs.get(scraper_name, {})

            # Create scraper instance
            scraper = scraper_class(scraper_config)

            # Execute search
            listings = scraper.search(location, min_price, max_price, **kwargs)

            execution_time = time.time() - start_time

            return {
                "success": True,
                "listings": listings,
                "execution_time": execution_time,
                "error": None,
            }

        except Exception as e:
            execution_time = time.time() - start_time
            self.logger.error(f"Error running {scraper_name}: {e}", exc_info=True)

            return {
                "success": False,
                "listings": [],
                "execution_time": execution_time,
                "error": str(e),
            }

    def _deduplicate_listings(
        self, listings: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Remove duplicate listings based on similarity.

        Args:
            listings: List of listings to deduplicate

        Returns:
            List of unique listings
        """
        if not listings:
            return []

        unique_listings = []
        seen_signatures: Set[str] = set()

        for listing in listings:
            # Create signature for exact matching
            signature = self._create_listing_signature(listing)

            if signature in seen_signatures:
                self.logger.debug(
                    f"Exact duplicate found: {listing.get('title', 'Unknown')}"
                )
                continue

            # Check for fuzzy duplicates
            if self._is_duplicate(listing, unique_listings):
                self.logger.debug(
                    f"Fuzzy duplicate found: {listing.get('title', 'Unknown')}"
                )
                continue

            # Add to unique listings
            unique_listings.append(listing)
            seen_signatures.add(signature)

        return unique_listings

    def _create_listing_signature(self, listing: Dict[str, Any]) -> str:
        """
        Create a signature for exact duplicate detection.

        Args:
            listing: Listing dictionary

        Returns:
            Signature string
        """
        # Use URL as primary signature (most reliable)
        if listing.get("url"):
            return listing["url"]

        # Fallback: combination of key fields
        title = (listing.get("title") or "").lower().strip()
        price = listing.get("price", 0)
        location = (listing.get("location") or "").lower().strip()

        return f"{title}|{price}|{location}"

    def _is_duplicate(
        self, listing: Dict[str, Any], existing_listings: List[Dict[str, Any]]
    ) -> bool:
        """
        Check if listing is a fuzzy duplicate of any existing listing.

        Args:
            listing: Listing to check
            existing_listings: List of already processed listings

        Returns:
            True if duplicate, False otherwise
        """
        for existing in existing_listings:
            if self._listings_similar(listing, existing):
                return True

        return False

    def _listings_similar(
        self, listing1: Dict[str, Any], listing2: Dict[str, Any]
    ) -> bool:
        """
        Check if two listings are similar enough to be considered duplicates.

        Args:
            listing1: First listing
            listing2: Second listing

        Returns:
            True if similar, False otherwise
        """
        # If both have URLs, they're only duplicates if URLs match
        if listing1.get("url") and listing2.get("url"):
            return listing1["url"] == listing2["url"]

        # Check price similarity (must be within 5% or $50)
        price1 = listing1.get("price", 0)
        price2 = listing2.get("price", 0)

        if price1 and price2:
            price_diff = abs(price1 - price2)
            price_threshold = min(max(price1, price2) * 0.05, 50)

            if price_diff > price_threshold:
                return False  # Prices too different

        # Check title similarity
        title1 = (listing1.get("title") or "").lower()
        title2 = (listing2.get("title") or "").lower()

        if title1 and title2:
            title_similarity = self._text_similarity(title1, title2)

            if title_similarity >= self.similarity_threshold:
                return True

        # Check location similarity
        location1 = (listing1.get("location") or "").lower()
        location2 = (listing2.get("location") or "").lower()

        if location1 and location2:
            location_similarity = self._text_similarity(location1, location2)

            # If title and location are both very similar, it's a duplicate
            if (
                title_similarity >= 0.7
                and location_similarity >= self.similarity_threshold
            ):
                return True

        return False

    def _text_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate similarity between two text strings.

        Args:
            text1: First text
            text2: Second text

        Returns:
            Similarity score between 0 and 1
        """
        return SequenceMatcher(None, text1, text2).ratio()

    def get_available_scrapers(self) -> List[str]:
        """
        Get list of available scraper names.

        Returns:
            List of scraper names
        """
        return list(self.AVAILABLE_SCRAPERS.keys())

    def get_enabled_scrapers(self) -> List[str]:
        """
        Get list of currently enabled scraper names.

        Returns:
            List of enabled scraper names
        """
        return self.enabled_scrapers.copy()

    def get_stats(self) -> Dict[str, Any]:
        """
        Get current statistics.

        Returns:
            Statistics dictionary
        """
        return self.stats.copy()

    def reset_stats(self):
        """Reset statistics counters."""
        self.stats = {
            "total_listings": 0,
            "unique_listings": 0,
            "duplicates_removed": 0,
            "scrapers_succeeded": 0,
            "scrapers_failed": 0,
            "execution_time": 0,
            "by_source": {},
        }


if __name__ == "__main__":
    # Test the scraper manager
    import logging
    import sys

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    print("=" * 70)
    print("Testing Scraper Manager")
    print("=" * 70)

    # Test configuration
    config = {
        "enabled_scrapers": ["kijiji", "realtor_ca"],  # Start with 2 fast ones
        "max_workers": 3,
        "deduplicate": True,
        "similarity_threshold": 0.85,
        "scraper_configs": {
            "rentals_ca": {"use_selenium": False}  # Disable Selenium for speed
        },
    }

    # Create manager
    manager = ScraperManager(config)

    print(f"\nAvailable scrapers: {', '.join(manager.get_available_scrapers())}")
    print(f"Enabled scrapers: {', '.join(manager.get_enabled_scrapers())}")
    print()

    # Test search
    test_location = "ottawa"
    test_min_price = 1000
    test_max_price = 2500

    print(f"Searching: {test_location}")
    print(f"Price range: ${test_min_price} - ${test_max_price}")
    print("-" * 70)

    # Execute search
    result = manager.search_all(test_location, test_min_price, test_max_price)

    # Display results
    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)

    stats = result["stats"]
    print(f"\nExecution time: {stats['execution_time']:.2f} seconds")
    print(f"Scrapers succeeded: {stats['scrapers_succeeded']}")
    print(f"Scrapers failed: {stats['scrapers_failed']}")
    print()

    print("Listings by source:")
    for source, count in stats["by_source"].items():
        print(f"  {source}: {count} listings")

    print()
    print(f"Total listings: {stats['total_listings']}")
    print(f"Duplicates removed: {stats['duplicates_removed']}")
    print(f"Unique listings: {stats['unique_listings']}")

    # Show errors if any
    if result["errors"]:
        print("\nErrors:")
        for scraper, error in result["errors"].items():
            print(f"  {scraper}: {error}")

    # Display first 5 listings
    print("\n" + "=" * 70)
    print("SAMPLE LISTINGS (First 5)")
    print("=" * 70)

    listings = result["listings"][:5]
    for i, listing in enumerate(listings, 1):
        print(f"\n{i}. {listing.get('title', 'No Title')}")
        print(f"   Source: {listing.get('source', 'Unknown')}")
        print(f"   Price: ${listing.get('price', 'N/A')}/month")
        print(f"   Location: {listing.get('location', 'N/A')}")
        print(f"   Bedrooms: {listing.get('bedrooms', 'N/A')}")
        print(f"   URL: {listing.get('url', 'N/A')[:80]}...")

    if len(result["listings"]) > 5:
        print(f"\n... and {len(result['listings']) - 5} more listings")

    print("\n" + "=" * 70)
    print("✓ Test complete!")
    print("=" * 70)
