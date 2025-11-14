"""
Kijiji Scraper
Scrapes rental listings from Kijiji.ca
"""

import json
import logging
from typing import Any, Dict, List, Optional

from bs4 import BeautifulSoup

from scrapers.base_scraper import BaseScraper


class KijijiScraper(BaseScraper):
    """Scraper for Kijiji.ca rental listings"""

    def get_source_name(self) -> str:
        """Return the source name"""
        return "kijiji"

    def build_search_url(
        self,
        location: str,
        min_price: Optional[int] = None,
        max_price: Optional[int] = None,
    ) -> str:
        """
        Build Kijiji search URL with filters.

        Args:
            location: City or area name
            min_price: Minimum monthly rent
            max_price: Maximum monthly rent

        Returns:
            Complete search URL with parameters
        """
        # Sanitize location for URL (e.g., 'City Of Toronto' -> 'city-of-toronto')
        location_slug = location.lower().replace(" ", "-").replace("_", "-")

        # Base URL for apartments-condos category (c37)
        base_url = "https://www.kijiji.ca/b-apartments-condos"

        # Construct URL: /b-apartments-condos/{location}/k0c37
        # k0 = all of location, c37 = apartments-condos category
        url = f"{base_url}/{location_slug}/k0c37"

        # Add price filter as URL parameter if provided
        # Kijiji uses '__' separator for price ranges (e.g., '1000__2000')
        if min_price or max_price:
            price_parts = []
            price_parts.append(str(min_price) if min_price else "")
            price_parts.append(str(max_price) if max_price else "")
            price_param = "__".join(price_parts)
            url += f"?price={price_param}"

        return url

    def parse_listings(self, html: str) -> List[Dict[str, Any]]:
        """
        Parse Kijiji HTML and extract listing data.

        Args:
            html: HTML content from Kijiji search page

        Returns:
            List of raw listing dictionaries
        """
        listings = []
        soup = BeautifulSoup(html, "html.parser")

        # Kijiji uses JSON-LD structured data
        json_ld_script = soup.find("script", type="application/ld+json")

        if not json_ld_script:
            self.logger.warning("JSON-LD script tag not found on Kijiji page")
            return listings

        try:
            data = json.loads(json_ld_script.string)

            # Verify it's an ItemList
            if data.get("@type") != "ItemList":
                self.logger.warning("JSON-LD data is not ItemList format")
                return listings

            item_list = data.get("itemListElement", [])
            self.logger.debug(f"Found {len(item_list)} items in JSON-LD")

            # Limit results to avoid excessive data
            max_listings = 25

            for item_entry in item_list[:max_listings]:
                item_details = item_entry.get("item", {})

                # Verify it's a rental property type
                item_type = item_details.get("@type", "")
                if item_type not in [
                    "SingleFamilyResidence",
                    "Apartment",
                    "Residence",
                    "House",
                ]:
                    continue

                # Extract listing data
                listing = {
                    "id": item_details.get("@id", ""),
                    "title": item_details.get("name", ""),
                    "url": item_details.get("url", ""),
                    "description": item_details.get("description", ""),
                }

                # Extract price from offers
                offers = item_details.get("offers", {})
                if isinstance(offers, list) and offers:
                    offers = offers[0]  # Take first offer if multiple

                if isinstance(offers, dict) and offers.get("@type") == "Offer":
                    price = offers.get("price")
                    currency = offers.get("priceCurrency", "CAD")
                    if price:
                        listing["price"] = price
                        listing["currency"] = currency

                # Extract location from address
                address_info = item_details.get("address")
                if isinstance(address_info, str):
                    listing["location"] = address_info
                elif isinstance(address_info, dict):
                    # Build address from components
                    parts = [
                        address_info.get("streetAddress"),
                        address_info.get("addressLocality"),
                        address_info.get("addressRegion"),
                        address_info.get("postalCode"),
                    ]
                    listing["location"] = ", ".join(filter(None, parts))

                # Extract image if available
                image = item_details.get("image")
                if image:
                    if isinstance(image, str):
                        listing["image"] = image
                    elif isinstance(image, list) and image:
                        listing["image"] = image[0]
                    elif isinstance(image, dict):
                        listing["image"] = image.get("url", "")

                # Only add if we have essential fields
                if listing.get("title") and listing.get("url"):
                    listings.append(listing)

        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to decode JSON-LD: {e}")
        except Exception as e:
            self.logger.error(f"Error parsing Kijiji listings: {e}", exc_info=True)

        return listings

    def standardize_listing(self, raw_listing: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert Kijiji listing to standardized format.

        Args:
            raw_listing: Raw listing data from parse_listings()

        Returns:
            Standardized listing dictionary
        """
        # Extract numeric price
        price = self._extract_price(raw_listing.get("price"))

        standardized = {
            "source": self.get_source_name(),
            "external_id": raw_listing.get("id", ""),
            "title": raw_listing.get("title", ""),
            "price": price,
            "location": raw_listing.get("location", ""),
            "url": raw_listing.get("url", ""),
            "description": raw_listing.get("description", ""),
            "image_url": raw_listing.get("image", ""),
            "bedrooms": None,  # Kijiji doesn't provide this in JSON-LD
            "bathrooms": None,
            "square_feet": None,
            "posted_date": None,  # Would need to parse from description or page
            "scraped_at": self._parse_date(None),  # Current time
        }

        return standardized


# Legacy function for backward compatibility
def scrape_kijiji(price_min=None, price_max=None, location=None):
    """
    Legacy function to maintain backward compatibility.

    Args:
        price_min: Minimum price
        price_max: Maximum price
        location: Location to search

    Returns:
        List of listings in old format
    """
    if not location:
        location = "canada"

    # Convert price to int if provided
    min_price = int(price_min) if price_min else None
    max_price = int(price_max) if price_max else None

    # Create scraper and search
    scraper = KijijiScraper()
    results = scraper.search(location, min_price, max_price)

    # Convert to old format for backward compatibility
    old_format = []
    for listing in results:
        old_format.append(
            {
                "title": listing.get("title", "N/A"),
                "price": f"${listing.get('price', 0):.2f}"
                if listing.get("price")
                else "N/A",
                "location": listing.get("location", "N/A"),
                "url": listing.get("url", "#"),
                "description": listing.get("description", "N/A"),
                "source": "Kijiji",
            }
        )

    return (
        old_format
        if old_format
        else [
            {
                "title": "No listings found",
                "price": "",
                "location": "",
                "url": "#",
                "description": "No listings found for the specified criteria",
                "source": "Kijiji",
            }
        ]
    )


if __name__ == "__main__":
    # Test the scraper
    import sys

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    print("Testing Kijiji Scraper...")
    print("-" * 50)

    # Test with Ottawa
    test_location = "ottawa"
    test_min_price = 1000
    test_max_price = 2500

    print(f"Searching: {test_location}")
    print(f"Price range: ${test_min_price} - ${test_max_price}")
    print("-" * 50)

    scraper = KijijiScraper({"save_debug_html": True})
    results = scraper.search(test_location, test_min_price, test_max_price)

    print(f"\nFound {len(results)} listings:\n")

    for i, listing in enumerate(results[:5], 1):  # Show first 5
        print(f"{i}. {listing['title']}")
        print(f"   Price: ${listing.get('price', 'N/A')}")
        print(f"   Location: {listing.get('location', 'N/A')}")
        print(f"   URL: {listing.get('url', 'N/A')}")
        print(f"   Description: {listing.get('description', 'N/A')[:100]}...")
        print()
