# This file makes 'scrapers' a Python package
from .kijiji_scraper import KijijiScraper, scrape_kijiji
from .realtor_ca_scraper import RealtorCAScraper
from .rentals_ca_scraper import RentalsCAScraper

__all__ = [
    "scrape_kijiji",
    "KijijiScraper",
    "RealtorCAScraper",
    "RentalsCAScraper",
]
