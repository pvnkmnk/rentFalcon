import logging
import time
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class BaseScraper(ABC):
    """
    Abstract base class for all rental listing scrapers.
    All site-specific scrapers should inherit from this class.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the scraper with configuration.

        Args:
            config: Dictionary containing scraper configuration
        """
        self.config = config or {}
        self.timeout = self.config.get("timeout", 30)
        self.max_retries = self.config.get("max_retries", 3)
        self.delay = self.config.get("delay", 1)
        self.user_agent = self.config.get(
            "user_agent",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        )
        self.save_debug = self.config.get("save_debug_html", False)
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

        # Initialize session with retry strategy
        self.session = self._create_session()
        self.last_request_time = 0

    def _create_session(self) -> requests.Session:
        """
        Create a requests session with retry strategy.

        Returns:
            Configured requests.Session object
        """
        session = requests.Session()

        # Retry strategy
        retry_strategy = Retry(
            total=self.max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"],
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        # Default headers
        session.headers.update(
            {
                "User-Agent": self.user_agent,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate, br",
                "DNT": "1",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
            }
        )

        return session

    def _rate_limit(self):
        """
        Implement rate limiting between requests.
        """
        elapsed = time.time() - self.last_request_time
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)
        self.last_request_time = time.time()

    @abstractmethod
    def get_source_name(self) -> str:
        """
        Get the name of the scraper source.

        Returns:
            String identifier for the source (e.g., "kijiji", "realtor_ca")
        """
        pass

    @abstractmethod
    def build_search_url(
        self,
        location: str,
        min_price: Optional[int] = None,
        max_price: Optional[int] = None,
    ) -> str:
        """
        Build the search URL for the specific site.

        Args:
            location: Location/city to search in
            min_price: Minimum price filter
            max_price: Maximum price filter

        Returns:
            Complete search URL
        """
        pass

    @abstractmethod
    def parse_listings(self, html: str) -> List[Dict[str, Any]]:
        """
        Parse HTML content and extract listings.

        Args:
            html: HTML content to parse

        Returns:
            List of dictionaries containing raw listing data
        """
        pass

    def search(
        self,
        location: str,
        min_price: Optional[int] = None,
        max_price: Optional[int] = None,
        **kwargs,
    ) -> List[Dict[str, Any]]:
        """
        Perform search and return standardized listings.

        Args:
            location: Location/city to search in
            min_price: Minimum price filter
            max_price: Maximum price filter
            **kwargs: Additional search parameters

        Returns:
            List of standardized listing dictionaries
        """
        try:
            self.logger.info(
                f"Starting search on {self.get_source_name()} - "
                f"Location: {location}, Price: ${min_price}-${max_price}"
            )

            # Build URL
            url = self.build_search_url(location, min_price, max_price)
            self.logger.debug(f"Search URL: {url}")

            # Rate limit
            self._rate_limit()

            # Fetch content
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()

            # Save debug HTML if enabled
            if self.save_debug:
                self._save_debug_html(response.text)

            # Parse listings
            raw_listings = self.parse_listings(response.text)
            self.logger.info(
                f"Found {len(raw_listings)} listings on {self.get_source_name()}"
            )

            # Standardize and filter
            standardized_listings = [
                self.standardize_listing(listing) for listing in raw_listings
            ]

            # Apply filters
            filtered_listings = self.filter_results(
                standardized_listings, min_price, max_price
            )

            self.logger.info(
                f"Returning {len(filtered_listings)} filtered listings from {self.get_source_name()}"
            )

            return filtered_listings

        except requests.RequestException as e:
            self.logger.error(f"Request error on {self.get_source_name()}: {str(e)}")
            return []
        except Exception as e:
            self.logger.error(
                f"Unexpected error on {self.get_source_name()}: {str(e)}",
                exc_info=True,
            )
            return []

    def standardize_listing(self, raw_listing: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert raw listing data to standardized format.

        Args:
            raw_listing: Raw listing data from parse_listings()

        Returns:
            Standardized listing dictionary with consistent field names
        """
        # Default implementation - can be overridden by subclasses
        standardized = {
            "source": self.get_source_name(),
            "external_id": raw_listing.get("id", ""),
            "title": raw_listing.get("title", ""),
            "price": self._extract_price(raw_listing.get("price")),
            "location": raw_listing.get("location", ""),
            "url": raw_listing.get("url", ""),
            "description": raw_listing.get("description", ""),
            "image_url": raw_listing.get("image", ""),
            "bedrooms": raw_listing.get("bedrooms"),
            "bathrooms": raw_listing.get("bathrooms"),
            "square_feet": raw_listing.get("square_feet"),
            "posted_date": self._parse_date(raw_listing.get("posted_date")),
            "scraped_at": datetime.utcnow(),
        }

        return standardized

    def filter_results(
        self,
        listings: List[Dict[str, Any]],
        min_price: Optional[int] = None,
        max_price: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        Filter listings by price range and other criteria.

        Args:
            listings: List of standardized listings
            min_price: Minimum price filter
            max_price: Maximum price filter

        Returns:
            Filtered list of listings
        """
        filtered = []

        for listing in listings:
            price = listing.get("price")

            # Skip if price is not available
            if price is None:
                continue

            # Apply price filters
            if min_price is not None and price < min_price:
                continue

            if max_price is not None and price > max_price:
                continue

            filtered.append(listing)

        return filtered

    def _extract_price(self, price_value: Any) -> Optional[float]:
        """
        Extract numeric price from various formats.

        Args:
            price_value: Price in various formats (string, int, float)

        Returns:
            Numeric price or None if cannot be extracted
        """
        if price_value is None:
            return None

        if isinstance(price_value, (int, float)):
            return float(price_value)

        if isinstance(price_value, str):
            # Remove currency symbols, commas, and extract number
            import re

            price_str = price_value.replace("$", "").replace(",", "").strip()
            match = re.search(r"\d+\.?\d*", price_str)
            if match:
                try:
                    return float(match.group())
                except ValueError:
                    pass

        return None

    def _parse_date(self, date_value: Any) -> Optional[datetime]:
        """
        Parse date from various formats.

        Args:
            date_value: Date in various formats

        Returns:
            datetime object or None
        """
        if date_value is None:
            return None

        if isinstance(date_value, datetime):
            return date_value

        if isinstance(date_value, str):
            # Try common date formats
            formats = [
                "%Y-%m-%d",
                "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%dT%H:%M:%SZ",
                "%Y-%m-%dT%H:%M:%S.%fZ",
                "%d/%m/%Y",
                "%m/%d/%Y",
            ]

            for fmt in formats:
                try:
                    return datetime.strptime(date_value, fmt)
                except ValueError:
                    continue

        return None

    def _save_debug_html(self, html: str):
        """
        Save HTML content for debugging purposes.

        Args:
            html: HTML content to save
        """
        try:
            import os

            debug_dir = self.config.get("debug_output_dir", "debug_output")
            os.makedirs(debug_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{debug_dir}/{self.get_source_name()}_{timestamp}.html"

            with open(filename, "w", encoding="utf-8") as f:
                f.write(html)

            self.logger.debug(f"Saved debug HTML to {filename}")
        except Exception as e:
            self.logger.warning(f"Failed to save debug HTML: {str(e)}")

    def close(self):
        """
        Clean up resources (close session, etc.)
        """
        if hasattr(self, "session"):
            self.session.close()

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
