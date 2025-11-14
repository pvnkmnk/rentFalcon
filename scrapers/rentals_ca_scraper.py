"""
Rentals.ca Scraper
Scrapes rental listings from Rentals.ca
Note: This site uses JavaScript rendering, so we attempt API detection first,
then fall back to Selenium if needed.
"""

import json
import logging
import re
import time
from datetime import datetime
from typing import Any, Dict, List, Optional

from scrapers.base_scraper import BaseScraper


class RentalsCAScraperException(Exception):
    """Custom exception for Rentals.ca scraper"""

    pass


class RentalsCAScraper(BaseScraper):
    """Scraper for Rentals.ca rental listings"""

    # Base URL
    BASE_URL = "https://rentals.ca"

    # Common city name mappings
    CITY_SLUGS = {
        "toronto": "toronto",
        "ottawa": "ottawa",
        "montreal": "montreal",
        "vancouver": "vancouver",
        "calgary": "calgary",
        "edmonton": "edmonton",
        "winnipeg": "winnipeg",
        "quebec city": "quebec-city",
        "hamilton": "hamilton",
        "kitchener": "kitchener",
        "london": "london",
        "victoria": "victoria",
        "halifax": "halifax",
        "saskatoon": "saskatoon",
        "regina": "regina",
        "windsor": "windsor",
        "oshawa": "oshawa",
        "barrie": "barrie",
        "kelowna": "kelowna",
        # Newmarket area (within 25km radius)
        "newmarket": "newmarket",
        "aurora": "aurora",
        "richmond hill": "richmond-hill",
        "east gwillimbury": "east-gwillimbury",
        "bradford": "bradford",
        "markham": "markham",
        "vaughan": "vaughan",
        "king city": "king-city",
    }

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Rentals.ca scraper.

        Args:
            config: Configuration dictionary
        """
        super().__init__(config)
        self.use_selenium = self.config.get("use_selenium", False)
        self._selenium_driver = None

    def get_source_name(self) -> str:
        """Return the source name"""
        return "rentals_ca"

    def _get_city_slug(self, location: str) -> str:
        """
        Convert location to Rentals.ca city slug.

        Args:
            location: City or area name

        Returns:
            URL-friendly city slug
        """
        location_lower = location.lower().strip()

        # Try exact match
        if location_lower in self.CITY_SLUGS:
            return self.CITY_SLUGS[location_lower]

        # Try partial match
        for city_name, slug in self.CITY_SLUGS.items():
            if city_name in location_lower or location_lower in city_name:
                return slug

        # Default: convert to slug format
        slug = location_lower.replace(" ", "-")
        self.logger.warning(
            f"City '{location}' not in known cities, using slug: {slug}"
        )
        return slug

    def build_search_url(
        self,
        location: str,
        min_price: Optional[int] = None,
        max_price: Optional[int] = None,
    ) -> str:
        """
        Build Rentals.ca search URL.

        Args:
            location: City or area name
            min_price: Minimum monthly rent
            max_price: Maximum monthly rent

        Returns:
            Complete search URL
        """
        city_slug = self._get_city_slug(location)
        url = f"{self.BASE_URL}/{city_slug}"

        # Rentals.ca uses query parameters for filtering
        # Note: Actual implementation may require bbox coordinates
        params = []

        if min_price:
            params.append(f"price_min={min_price}")

        if max_price:
            params.append(f"price_max={max_price}")

        if params:
            url += "?" + "&".join(params)

        return url

    def _try_api_approach(
        self, location: str, min_price: Optional[int], max_price: Optional[int]
    ) -> List[Dict[str, Any]]:
        """
        Attempt to find and use internal API endpoints.

        Args:
            location: City name
            min_price: Minimum price
            max_price: Maximum price

        Returns:
            List of listings if API found, empty list otherwise
        """
        try:
            city_slug = self._get_city_slug(location)

            # Try to find API endpoint pattern
            # Many React/Vue apps use patterns like /api/listings or /graphql
            api_urls = [
                f"{self.BASE_URL}/api/listings/{city_slug}",
                f"{self.BASE_URL}/api/search?city={city_slug}",
                f"{self.BASE_URL}/graphql",
            ]

            for api_url in api_urls:
                try:
                    self.logger.debug(f"Trying API endpoint: {api_url}")
                    response = self.session.get(api_url, timeout=self.timeout)

                    if response.status_code == 200:
                        data = response.json()
                        # Check if response looks like listing data
                        if isinstance(data, dict) and any(
                            k in data for k in ["listings", "results", "data"]
                        ):
                            self.logger.info(f"Found API endpoint: {api_url}")
                            return self._extract_from_api_response(data)
                        elif isinstance(data, list) and len(data) > 0:
                            return self._extract_from_api_response({"listings": data})

                except Exception as e:
                    self.logger.debug(f"API endpoint {api_url} failed: {e}")
                    continue

        except Exception as e:
            self.logger.debug(f"API approach failed: {e}")

        return []

    def _extract_from_api_response(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract listings from API response.

        Args:
            data: JSON response data

        Returns:
            List of listing dictionaries
        """
        listings = []

        # Try different common response structures
        items = (
            data.get("listings")
            or data.get("results")
            or data.get("data", {}).get("listings")
            or data.get("data", {}).get("results")
            or []
        )

        for item in items:
            listing = {
                "id": item.get("id") or item.get("listing_id"),
                "title": item.get("title") or item.get("name"),
                "price": item.get("price") or item.get("rent"),
                "location": item.get("location")
                or item.get("address")
                or item.get("city"),
                "url": item.get("url") or item.get("link"),
                "description": item.get("description"),
                "bedrooms": item.get("bedrooms") or item.get("beds"),
                "bathrooms": item.get("bathrooms") or item.get("baths"),
                "square_feet": item.get("square_feet") or item.get("sqft"),
                "image": item.get("image") or item.get("photo"),
            }

            if listing.get("title") or listing.get("id"):
                listings.append(listing)

        return listings

    def _use_selenium_approach(self, url: str) -> List[Dict[str, Any]]:
        """
        Use Selenium to render page and extract data.

        Args:
            url: URL to scrape

        Returns:
            List of listing dictionaries
        """
        try:
            from selenium import webdriver
            from selenium.common.exceptions import TimeoutException
            from selenium.webdriver.chrome.service import Service
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.support.ui import WebDriverWait
            from webdriver_manager.chrome import ChromeDriverManager

            self.logger.info("Using Selenium to render page...")

            # Setup Chrome options
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument(f"user-agent={self.user_agent}")

            # Auto-detect Chrome binary location (Windows)
            import os

            chrome_paths = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                os.path.expanduser(
                    r"~\AppData\Local\Google\Chrome\Application\chrome.exe"
                ),
            ]
            for chrome_path in chrome_paths:
                if os.path.exists(chrome_path):
                    options.binary_location = chrome_path
                    self.logger.info(f"Found Chrome at: {chrome_path}")
                    break

            # Create driver with webdriver-manager for automatic ChromeDriver installation
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            driver.set_page_load_timeout(30)

            try:
                driver.get(url)

                # Wait for listings to load
                wait = WebDriverWait(driver, 10)
                wait.until(
                    EC.presence_of_element_located((By.CLASS_NAME, "listing-card"))
                )

                # Additional wait for JS to complete
                time.sleep(2)

                # Get page source and parse
                html = driver.page_source
                listings = self.parse_listings(html)

                return listings

            finally:
                driver.quit()

        except ImportError:
            self.logger.error(
                "Selenium not installed. Install with: pip install selenium webdriver-manager"
            )
            raise RentalsCAScraperException(
                "Selenium required for Rentals.ca but not installed"
            )
        except Exception as e:
            self.logger.error(f"Selenium approach failed: {e}")
            raise

    def search(
        self,
        location: str,
        min_price: Optional[int] = None,
        max_price: Optional[int] = None,
        **kwargs,
    ) -> List[Dict[str, Any]]:
        """
        Search for rental listings.

        Args:
            location: City to search in
            min_price: Minimum price
            max_price: Maximum price
            **kwargs: Additional parameters

        Returns:
            List of standardized listings
        """
        try:
            self.logger.info(
                f"Starting search on {self.get_source_name()} - "
                f"Location: {location}, Price: ${min_price}-${max_price}"
            )

            # Try API approach first
            self.logger.info("Attempting API approach...")
            raw_listings = self._try_api_approach(location, min_price, max_price)

            # If API approach failed, try Selenium
            if not raw_listings:
                self.logger.warning(
                    "API approach failed or returned no results. "
                    "Rentals.ca requires Selenium for scraping."
                )
                self.logger.info(
                    "Note: To enable Selenium, install it with: "
                    "pip install selenium webdriver-manager"
                )

                if self.use_selenium:
                    url = self.build_search_url(location, min_price, max_price)
                    raw_listings = self._use_selenium_approach(url)
                else:
                    self.logger.error(
                        "Selenium is required but not enabled. "
                        "Set use_selenium=True in config."
                    )
                    return []

            self.logger.info(
                f"Found {len(raw_listings)} raw listings from {self.get_source_name()}"
            )

            # Standardize listings
            standardized_listings = [
                self.standardize_listing(listing) for listing in raw_listings
            ]

            # Filter by price
            filtered_listings = self.filter_results(
                standardized_listings, min_price, max_price
            )

            self.logger.info(f"Returning {len(filtered_listings)} filtered listings")

            return filtered_listings

        except Exception as e:
            self.logger.error(f"Error searching {self.get_source_name()}: {e}")
            return []

    def parse_listings(self, html: str) -> List[Dict[str, Any]]:
        """
        Parse HTML and extract listing data.

        Args:
            html: HTML content

        Returns:
            List of raw listing dictionaries
        """
        from bs4 import BeautifulSoup

        listings = []
        soup = BeautifulSoup(html, "html.parser")

        # Find listing cards (adjust selectors based on actual site structure)
        listing_cards = soup.find_all("div", class_=re.compile("listing-card"))

        if not listing_cards:
            # Try alternative selectors
            listing_cards = soup.find_all("div", {"data-listing": True})

        if not listing_cards:
            listing_cards = soup.find_all("article", class_=re.compile("listing"))

        self.logger.debug(f"Found {len(listing_cards)} listing cards in HTML")

        for card in listing_cards:
            try:
                listing = {}

                # Extract ID
                listing["id"] = (
                    card.get("data-id")
                    or card.get("data-listing-id")
                    or card.get("id", "")
                )

                # Extract title
                title_elem = (
                    card.find("h2")
                    or card.find("h3")
                    or card.find(class_=re.compile("title"))
                )
                if title_elem:
                    listing["title"] = title_elem.get_text(strip=True)

                # Extract price
                price_elem = card.find(class_=re.compile("price"))
                if price_elem:
                    listing["price"] = price_elem.get_text(strip=True)

                # Extract location
                location_elem = card.find(class_=re.compile("location|address"))
                if location_elem:
                    listing["location"] = location_elem.get_text(strip=True)

                # Extract URL
                link_elem = card.find("a", href=True)
                if link_elem:
                    href = link_elem["href"]
                    if href.startswith("/"):
                        href = self.BASE_URL + href
                    listing["url"] = href

                # Extract image
                img_elem = card.find("img")
                if img_elem:
                    listing["image"] = img_elem.get("src") or img_elem.get("data-src")

                # Extract bedrooms
                beds_elem = card.find(class_=re.compile("bed"))
                if beds_elem:
                    beds_text = beds_elem.get_text(strip=True)
                    beds_match = re.search(r"(\d+)", beds_text)
                    if beds_match:
                        listing["bedrooms"] = int(beds_match.group(1))

                # Extract bathrooms
                baths_elem = card.find(class_=re.compile("bath"))
                if baths_elem:
                    baths_text = baths_elem.get_text(strip=True)
                    baths_match = re.search(r"(\d+\.?\d*)", baths_text)
                    if baths_match:
                        listing["bathrooms"] = float(baths_match.group(1))

                # Only add if we have at least title or URL
                if listing.get("title") or listing.get("url"):
                    listings.append(listing)

            except Exception as e:
                self.logger.debug(f"Error parsing listing card: {e}")
                continue

        return listings

    def standardize_listing(self, raw_listing: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert raw listing to standardized format.

        Args:
            raw_listing: Raw listing data

        Returns:
            Standardized listing dictionary
        """
        # Extract numeric price
        price = self._extract_price(raw_listing.get("price"))

        # Build title if needed
        title = raw_listing.get("title") or self._build_title(raw_listing)

        standardized = {
            "source": self.get_source_name(),
            "external_id": str(raw_listing.get("id", "")),
            "title": title,
            "price": price,
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

    def _build_title(self, raw_listing: Dict[str, Any]) -> str:
        """
        Build a title from listing data.

        Args:
            raw_listing: Raw listing data

        Returns:
            Generated title string
        """
        parts = []

        bedrooms = raw_listing.get("bedrooms")
        if bedrooms:
            parts.append(f"{bedrooms} Bedroom")

        location = raw_listing.get("location", "")
        if location:
            parts.append(f"in {location}")

        return " ".join(parts) if parts else "Rental Property"

    def close(self):
        """Clean up resources"""
        if self._selenium_driver:
            try:
                self._selenium_driver.quit()
            except:
                pass
        super().close()


if __name__ == "__main__":
    # Test the scraper
    import logging
    import sys

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    print("Testing Rentals.ca Scraper...")
    print("-" * 50)
    print("\n⚠️  NOTE: Rentals.ca requires Selenium for scraping")
    print("Install with: pip install selenium webdriver-manager")
    print("-" * 50)

    # Test with Ottawa
    test_location = "ottawa"
    test_min_price = 1000
    test_max_price = 2500

    print(f"\nSearching: {test_location}")
    print(f"Price range: ${test_min_price} - ${test_max_price}")
    print("-" * 50)

    # Try without Selenium first (will show warning)
    scraper = RentalsCAScraper({"save_debug_html": True, "use_selenium": False})
    results = scraper.search(test_location, test_min_price, test_max_price)

    if not results:
        print("\n❌ No results found without Selenium")
        print("\nTo enable Selenium scraping:")
        print("1. Install Selenium: pip install selenium webdriver-manager")
        print("2. Set use_selenium=True in config")
        print("\nExample:")
        print("  scraper = RentalsCAScraper({'use_selenium': True})")
        print("  results = scraper.search('ottawa', 1000, 2500)")
    else:
        print(f"\n✓ Found {len(results)} listings:\n")

        for i, listing in enumerate(results[:5], 1):
            print(f"{i}. {listing['title']}")
            print(f"   Price: ${listing.get('price', 'N/A')}")
            print(f"   Bedrooms: {listing.get('bedrooms', 'N/A')}")
            print(f"   Location: {listing.get('location', 'N/A')}")
            print(f"   URL: {listing.get('url', 'N/A')}")
            print()
