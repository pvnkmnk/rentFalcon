"""
Realtor.ca Scraper (HTML Version with Selenium Fallback)
Scrapes rental listings from Realtor.ca using HTML parsing with Selenium fallback
"""

import json
import logging
import os
import re
import time
from datetime import datetime
from typing import Any, Dict, List, Optional
from urllib.parse import urlencode

from bs4 import BeautifulSoup

from scrapers.base_scraper import BaseScraper


class RealtorCAScraper(BaseScraper):
    """Scraper for Realtor.ca rental listings using HTML parsing"""

    # Base URL for map view (returns listings)
    BASE_URL = "https://www.realtor.ca/map"

    # Major Canadian cities with approximate bounding boxes
    # Format: (lat_min, lat_max, lon_min, lon_max)
    CITY_COORDINATES = {
        "toronto": (43.581, 43.855, -79.639, -79.116),
        "ottawa": (45.247, 45.535, -75.927, -75.247),
        "montreal": (45.410, 45.704, -73.980, -73.475),
        "vancouver": (49.198, 49.316, -123.224, -122.986),
        "calgary": (50.842, 51.211, -114.310, -113.895),
        "edmonton": (53.396, 53.711, -113.699, -113.297),
        "winnipeg": (49.766, 49.978, -97.325, -97.065),
        "quebec": (46.761, 46.862, -71.307, -71.155),
        "hamilton": (43.200, 43.311, -79.987, -79.714),
        "kitchener": (43.400, 43.510, -80.560, -80.420),
        "london": (42.900, 43.050, -81.350, -81.150),
        "victoria": (48.400, 48.500, -123.450, -123.300),
        "windsor": (42.250, 42.350, -83.100, -82.900),
        "oshawa": (43.850, 43.950, -78.950, -78.800),
        "saskatoon": (52.050, 52.230, -106.750, -106.550),
        "regina": (50.400, 50.500, -104.700, -104.500),
        "halifax": (44.600, 44.700, -63.700, -63.500),
        "barrie": (44.350, 44.450, -79.750, -79.600),
        "guelph": (43.500, 43.600, -80.300, -80.150),
        "kingston": (44.200, 44.300, -76.600, -76.450),
        # Newmarket area (within 25km radius)
        "newmarket": (43.990, 44.090, -79.530, -79.390),
        "aurora": (43.930, 44.030, -79.530, -79.390),
        "richmond hill": (43.820, 43.920, -79.510, -79.370),
        "east gwillimbury": (44.040, 44.140, -79.500, -79.360),
        "bradford": (44.070, 44.170, -79.630, -79.490),
        "markham": (43.810, 43.910, -79.410, -79.270),
        "vaughan": (43.790, 43.890, -79.570, -79.430),
        "king city": (43.880, 43.980, -79.600, -79.460),
    }

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Realtor.ca scraper.

        Args:
            config: Configuration dictionary
        """
        super().__init__(config)
        self.use_selenium = self.config.get("use_selenium", True)
        self._selenium_driver = None

    def get_source_name(self) -> str:
        """Return the source name"""
        return "realtor_ca"

    def _get_coordinates(self, location: str) -> Optional[tuple]:
        """
        Get bounding box coordinates for a location.

        Args:
            location: City or area name

        Returns:
            Tuple of (lat_min, lat_max, lon_min, lon_max) or None
        """
        location_lower = location.lower().strip()

        # Try exact match
        if location_lower in self.CITY_COORDINATES:
            return self.CITY_COORDINATES[location_lower]

        # Try partial match
        for city_name, coords in self.CITY_COORDINATES.items():
            if city_name in location_lower or location_lower in city_name:
                return coords

        # Default to Toronto if no match found (largest rental market)
        self.logger.warning(
            f"Location '{location}' not found in known cities, defaulting to Toronto"
        )
        return self.CITY_COORDINATES["toronto"]

    def build_search_url(
        self,
        location: str,
        min_price: Optional[int] = None,
        max_price: Optional[int] = None,
    ) -> str:
        """
        Build Realtor.ca search URL with filters.

        Args:
            location: City or area name
            min_price: Minimum monthly rent
            max_price: Maximum monthly rent

        Returns:
            Complete search URL with parameters
        """
        coords = self._get_coordinates(location)
        if not coords:
            raise ValueError(
                f"Could not determine coordinates for location: {location}"
            )

        lat_min, lat_max, lon_min, lon_max = coords

        # Calculate center point
        center_lat = (lat_min + lat_max) / 2
        center_lon = (lon_min + lon_max) / 2

        # Build URL parameters
        params = {
            "ZoomLevel": "12",
            "Center": f"{center_lat:.3f}%2C{center_lon:.3f}",
            "LatitudeMax": f"{lat_max:.3f}",
            "LongitudeMax": f"{lon_max:.3f}",
            "LatitudeMin": f"{lat_min:.3f}",
            "LongitudeMin": f"{lon_min:.3f}",
            "Sort": "6-D",  # Sort by date (newest first)
            "PropertyTypeGroupID": "1",  # Residential
            "PropertySearchTypeId": "1",  # No preference
            "TransactionTypeId": "3",  # For Rent
            "Currency": "CAD",
            "RecordsPerPage": "50",
        }

        # Add price filters if provided
        if min_price:
            params["PriceMin"] = str(min_price)
        if max_price:
            params["PriceMax"] = str(max_price)

        # Build URL
        url = f"{self.BASE_URL}#{urlencode(params, safe='%,')}"
        return url

    def parse_listings(self, html: str) -> List[Dict[str, Any]]:
        """
        Parse Realtor.ca HTML and extract listing data.

        Args:
            html: HTML content from Realtor.ca

        Returns:
            List of raw listing dictionaries
        """
        listings = []
        soup = BeautifulSoup(html, "html.parser")

        # Try to find embedded JSON data (Realtor.ca embeds data in script tags)
        # Look for window.__INITIAL_STATE__ or similar
        scripts = soup.find_all("script")

        for script in scripts:
            if script.string and (
                "listings" in script.string.lower()
                or "results" in script.string.lower()
            ):
                try:
                    # Try to extract JSON from script content
                    script_content = script.string

                    # Look for JSON object patterns
                    # Pattern 1: window.__INITIAL_STATE__ = {...}
                    match = re.search(
                        r"window\.__INITIAL_STATE__\s*=\s*({.*?});",
                        script_content,
                        re.DOTALL,
                    )
                    if not match:
                        # Pattern 2: var data = {...}
                        match = re.search(
                            r"var\s+\w+\s*=\s*({.*?});", script_content, re.DOTALL
                        )

                    if match:
                        json_str = match.group(1)
                        data = json.loads(json_str)

                        # Extract listings from nested structure
                        extracted = self._extract_from_json(data)
                        if extracted:
                            listings.extend(extracted)
                            self.logger.debug(
                                f"Extracted {len(extracted)} listings from embedded JSON"
                            )

                except (json.JSONDecodeError, AttributeError) as e:
                    self.logger.debug(f"Could not parse JSON from script: {e}")
                    continue

        # Fallback: Parse HTML structure if JSON extraction failed
        if not listings:
            self.logger.info("JSON extraction failed, attempting HTML parsing fallback")
            listings = self._parse_html_structure(soup)

        return listings[:25]  # Limit to 25 listings

    def _extract_from_json(self, data: Any) -> List[Dict[str, Any]]:
        """
        Recursively search for listings in JSON structure.

        Args:
            data: JSON data structure

        Returns:
            List of listing dictionaries
        """
        listings = []

        if isinstance(data, dict):
            # Check if this dict looks like a listing
            if "MlsNumber" in data or "Price" in data:
                listing = self._parse_json_listing(data)
                if listing:
                    listings.append(listing)

            # Recursively search in dict values
            for key, value in data.items():
                if key.lower() in ["results", "listings", "pins", "properties"]:
                    listings.extend(self._extract_from_json(value))

        elif isinstance(data, list):
            # Recursively search in list items
            for item in data:
                listings.extend(self._extract_from_json(item))

        return listings

    def _parse_json_listing(
        self, listing_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Parse a single listing from JSON format.

        Args:
            listing_data: Raw listing data from JSON

        Returns:
            Parsed listing dictionary or None
        """
        try:
            # Extract relevant fields
            mls_number = listing_data.get("MlsNumber", listing_data.get("Id", ""))
            price = listing_data.get("Price", listing_data.get("price"))

            # Get address
            address_data = listing_data.get("Property", {}).get("Address", {})
            if not address_data and "Address" in listing_data:
                address_data = listing_data["Address"]

            address = address_data.get("AddressText", "")
            city = address_data.get("City", "")
            province = address_data.get("Province", "")

            full_address = f"{address}, {city}, {province}".strip(", ")

            # Get building data
            building_data = listing_data.get("Building", {})
            bedrooms = building_data.get("Bedrooms", building_data.get("BedroomsTotal"))
            bathrooms = building_data.get(
                "BathroomTotal", building_data.get("Bathrooms")
            )

            # Get property details
            property_data = listing_data.get("Property", {})
            property_type = property_data.get("Type", "")

            # Build URL
            relative_url = listing_data.get("RelativeDetailsURL", "")
            url = f"https://www.realtor.ca{relative_url}" if relative_url else ""

            # Get photo
            photo = (
                listing_data.get("Property", {})
                .get("Photo", [{}])[0]
                .get("HighResPath", "")
            )
            if not photo:
                photo = listing_data.get("Photo", [{}])[0].get("HighResPath", "")

            return {
                "id": mls_number,
                "title": f"{bedrooms or '?'} Bed, {bathrooms or '?'} Bath {property_type} in {city}",
                "price": price,
                "location": full_address,
                "url": url,
                "bedrooms": bedrooms,
                "bathrooms": bathrooms,
                "image": f"https:{photo}"
                if photo and not photo.startswith("http")
                else photo,
                "description": property_type,
            }

        except Exception as e:
            self.logger.debug(f"Error parsing listing: {e}")
            return None

    def _parse_html_structure(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """
        Fallback HTML parsing if JSON extraction fails.

        Args:
            soup: BeautifulSoup object

        Returns:
            List of listing dictionaries
        """
        listings = []

        # Try to find listing cards in HTML
        # Realtor.ca uses various class names, try common patterns
        card_selectors = [
            ".listingCard",
            "[class*='listing-card']",
            "[class*='propertyCard']",
            ".cardCon",
        ]

        cards = []
        for selector in card_selectors:
            cards = soup.select(selector)
            if cards:
                self.logger.debug(f"Found {len(cards)} cards with selector: {selector}")
                break

        for card in cards[:25]:
            try:
                # Extract price
                price_elem = card.select_one(".listingCardPrice, [class*='price']")
                price_text = price_elem.get_text(strip=True) if price_elem else ""

                # Extract address
                address_elem = card.select_one(
                    ".listingCardAddress, [class*='address']"
                )
                address = address_elem.get_text(strip=True) if address_elem else ""

                # Extract URL
                link_elem = card.select_one("a[href*='/property-details']")
                url = ""
                if link_elem and link_elem.get("href"):
                    url = f"https://www.realtor.ca{link_elem['href']}"

                # Extract image
                img_elem = card.select_one("img")
                image = img_elem.get("src", "") if img_elem else ""

                # Extract bedrooms/bathrooms
                details_text = card.get_text()
                bed_match = re.search(r"(\d+)\s*(?:bed|br)", details_text, re.I)
                bath_match = re.search(r"(\d+)\s*(?:bath|ba)", details_text, re.I)

                bedrooms = int(bed_match.group(1)) if bed_match else None
                bathrooms = int(bath_match.group(1)) if bath_match else None

                if price_text or address:
                    listings.append(
                        {
                            "id": url.split("/")[-1] if url else "",
                            "title": f"{bedrooms or '?'} Bed Rental in {address.split(',')[0] if address else 'Unknown'}",
                            "price": price_text,
                            "location": address,
                            "url": url,
                            "bedrooms": bedrooms,
                            "bathrooms": bathrooms,
                            "image": image,
                            "description": "",
                        }
                    )

            except Exception as e:
                self.logger.debug(f"Error parsing card: {e}")
                continue

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

            self.logger.info("Using Selenium to render Realtor.ca page...")

            # Setup Chrome options
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument(f"user-agent={self.user_agent}")
            options.add_argument("--disable-blink-features=AutomationControlled")

            # Auto-detect Chrome binary location (Windows)
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

                # Wait for content to load
                time.sleep(5)  # Give extra time for map/listings to render

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
            return []
        except Exception as e:
            self.logger.error(f"Selenium approach failed: {e}")
            return []

    def _selenium_search_fallback(
        self, url: str, min_price: Optional[int] = None, max_price: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Fallback to Selenium when regular requests fail.

        Args:
            url: URL to scrape
            min_price: Minimum price filter
            max_price: Maximum price filter

        Returns:
            List of standardized listing dictionaries
        """
        try:
            raw_listings = self._use_selenium_approach(url)

            # Standardize and filter
            standardized_listings = [
                self.standardize_listing(listing) for listing in raw_listings
            ]

            # Apply filters
            filtered_listings = self.filter_results(
                standardized_listings, min_price, max_price
            )

            return filtered_listings
        except Exception as e:
            self.logger.error(f"Selenium fallback failed: {e}")
            return []

    def search(
        self,
        location: str,
        min_price: Optional[int] = None,
        max_price: Optional[int] = None,
        **kwargs,
    ) -> List[Dict[str, Any]]:
        """
        Override search method with better error handling for Realtor.ca.

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

            # Fetch content with enhanced headers
            headers = {
                "User-Agent": self.user_agent,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate, br",
                "DNT": "1",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Cache-Control": "max-age=0",
            }

            response = self.session.get(url, headers=headers, timeout=self.timeout)

            # Check for various error codes
            if response.status_code == 403:
                self.logger.warning(
                    "Realtor.ca returned 403 Forbidden - trying Selenium fallback..."
                )
                if self.use_selenium:
                    return self._selenium_search_fallback(url, min_price, max_price)
                return []

            response.raise_for_status()

            # Save debug HTML if enabled
            if self.save_debug:
                self._save_debug_html(response.text)

            # Parse listings
            raw_listings = self.parse_listings(response.text)

            # If no results and Selenium is enabled, try Selenium approach
            if not raw_listings and self.use_selenium:
                self.logger.info(
                    "HTML parsing returned no results, trying Selenium approach..."
                )
                raw_listings = self._use_selenium_approach(url)

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

        except Exception as e:
            self.logger.error(f"Error searching {self.get_source_name()}: {str(e)}")
            # Don't return error details to avoid exposing scraping issues
            return []

    def close(self):
        """Clean up resources"""
        super().close()
        if self._selenium_driver:
            try:
                self._selenium_driver.quit()
            except:
                pass


# Test function
if __name__ == "__main__":
    import logging
    import sys

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    print("Testing Realtor.ca Scraper...")
    print("-" * 50)

    # Test location
    test_location = "newmarket"
    test_min_price = 1500
    test_max_price = 2500

    print(f"\nSearching for rentals in {test_location}")
    print(f"Price range: ${test_min_price} - ${test_max_price}")
    print("-" * 50)

    scraper = RealtorCAScraper({"save_debug_html": True})
    results = scraper.search(test_location, test_min_price, test_max_price)

    print(f"\nFound {len(results)} listings")
    print("-" * 50)

    for i, listing in enumerate(results[:5], 1):
        print(f"\n{i}. {listing.get('title', 'No title')}")
        print(f"   Price: ${listing.get('price', 'N/A')}")
        print(f"   Location: {listing.get('location', 'N/A')}")
        print(f"   Bedrooms: {listing.get('bedrooms', 'N/A')}")
        print(f"   URL: {listing.get('url', 'N/A')}")

    scraper.close()
