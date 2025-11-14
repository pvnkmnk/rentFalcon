# Rental Scanner - Scraper Guide

## Overview

This guide covers testing, using, and implementing scrapers for the Rental Scanner application. Currently implemented scrapers:

1. ✅ **Kijiji** - HTML parsing (JSON-LD structured data)
2. ✅ **Realtor.ca** - API-based (using official API endpoint)

Coming soon: Rentals.ca, Viewit.ca, Apartments.ca

---

## Table of Contents

- [Quick Start](#quick-start)
- [Testing Scrapers](#testing-scrapers)
- [How Scrapers Work](#how-scrapers-work)
- [Scraper Details](#scraper-details)
- [Adding New Scrapers](#adding-new-scrapers)
- [Troubleshooting](#troubleshooting)

---

## Quick Start

### Prerequisites

```bash
# Ensure you have Python 3.11+ installed
python --version

# Install dependencies
pip install -r requirements.txt
```

### Test All Scrapers

```bash
# Run the test suite
python test_scrapers.py
```

This will test both Kijiji and Realtor.ca scrapers and show sample results.

### Test Individual Scrapers

**Test Kijiji:**
```bash
python scrapers/kijiji_scraper.py
```

**Test Realtor.ca:**
```bash
python scrapers/realtor_ca_scraper.py
```

---

## Testing Scrapers

### Using the Test Suite

The `test_scrapers.py` script provides comprehensive testing:

```bash
python test_scrapers.py
```

**Expected Output:**
```
==================================================================
  Rental Scanner - Scraper Test Suite
==================================================================
Started at: 2024-01-15 10:30:00

==================================================================
  Testing Kijiji Scraper
==================================================================
Search Parameters:
  Location: ottawa
  Price Range: $1000 - $2500

✓ Found 15 listings from Kijiji

1. Beautiful 2 Bedroom Apartment in Downtown Ottawa
   Price: $1800.00
   Location: Ottawa, ON
   URL: https://www.kijiji.ca/...

... and 12 more listings

==================================================================
  Testing Realtor.ca Scraper
==================================================================
...
```

### Manual Testing

**Python Interactive Shell:**
```python
from scrapers.kijiji_scraper import KijijiScraper
from scrapers.realtor_ca_scraper import RealtorCAScraper

# Test Kijiji
kijiji = KijijiScraper()
results = kijiji.search('ottawa', 1000, 2500)
print(f"Found {len(results)} listings")

# Test Realtor.ca
realtor = RealtorCAScraper()
results = realtor.search('toronto', 1500, 3000)
print(f"Found {len(results)} listings")
```

### Debug Mode

Enable debug output to see detailed information:

```python
from scrapers.kijiji_scraper import KijijiScraper

scraper = KijijiScraper({
    'save_debug_html': True,      # Save HTML/JSON responses
    'debug_output_dir': 'debug',  # Output directory
})

results = scraper.search('ottawa', 1000, 2000)
# Check debug/ folder for saved responses
```

---

## How Scrapers Work

### Architecture

All scrapers inherit from `BaseScraper` which provides:
- Rate limiting
- Error handling and retries
- Standardized data format
- Debug capabilities
- Logging

### Data Flow

```
User Input (location, price range)
    ↓
Scraper.search()
    ↓
Build search URL/API payload
    ↓
HTTP Request (with rate limiting)
    ↓
Parse response (HTML or JSON)
    ↓
Extract raw listing data
    ↓
Standardize format
    ↓
Filter by criteria
    ↓
Return standardized listings
```

### Standardized Output Format

All scrapers return listings in this format:

```python
{
    'source': 'kijiji',              # Source identifier
    'external_id': '1234567890',     # MLS#, listing ID, etc.
    'title': '2 Bed Apartment...',   # Listing title
    'price': 1800.0,                 # Monthly rent (float)
    'location': 'Ottawa, ON',        # Full address/location
    'url': 'https://...',            # Direct link to listing
    'description': 'Beautiful...',   # Full description
    'image_url': 'https://...',      # Main image URL
    'bedrooms': 2,                   # Number of bedrooms (int or None)
    'bathrooms': 1.5,                # Number of bathrooms (float or None)
    'square_feet': 950,              # Size in sq ft (int or None)
    'posted_date': datetime(...),    # When posted (datetime or None)
    'scraped_at': datetime(...)      # When scraped (datetime)
}
```

---

## Scraper Details

### 1. Kijiji Scraper

**Type:** HTML Parsing (BeautifulSoup)  
**Data Source:** JSON-LD structured data embedded in HTML  
**Reliability:** High (structured data is stable)

**How it works:**
1. Builds search URL with location slug and price parameters
2. Fetches HTML page
3. Extracts JSON-LD `<script>` tag containing structured data
4. Parses ItemList with property listings
5. Standardizes and filters results

**Example URL:**
```
https://www.kijiji.ca/b-apartments-condos/ottawa/k0c37?price=1000__2500
```

**Location Format:**
- Use city names: `ottawa`, `toronto`, `vancouver`
- Multi-word cities: `north-york`, `saint-john`
- Common slugs work: `gta-greater-toronto-area`

**Price Filtering:**
- Uses `__` separator: `min__max`
- Examples: `1000__2000`, `__1500` (max only), `1000__` (min only)

**Known Limitations:**
- No bedroom/bathroom data in JSON-LD
- Location resolution may vary by city
- Rate limiting after ~50 requests/hour

**Code Example:**
```python
from scrapers.kijiji_scraper import KijijiScraper

scraper = KijijiScraper()
listings = scraper.search(
    location='ottawa',
    min_price=1000,
    max_price=2500
)

for listing in listings:
    print(f"{listing['title']} - ${listing['price']}")
```

---

### 2. Realtor.ca Scraper

**Type:** API-based (JSON REST API)  
**Data Source:** Official Realtor.ca API  
**Reliability:** Very High (official API with structured data)

**How it works:**
1. Maps location to geographic bounding box (lat/lon coordinates)
2. Builds JSON API payload with search parameters
3. POSTs to API endpoint
4. Parses JSON response
5. Extracts detailed listing information
6. Standardizes and returns results

**API Endpoint:**
```
POST https://api2.realtor.ca/Listing.svc/PropertySearch_Post
```

**Supported Locations:**
Pre-configured coordinates for major cities:
- Toronto, Ottawa, Montreal, Vancouver
- Calgary, Edmonton, Winnipeg, Quebec City
- Hamilton, Kitchener, London, Victoria
- Windsor, Oshawa, Saskatoon, Regina
- Halifax, Barrie, Guelph, Kingston

**API Parameters:**
```python
{
    'CultureId': 1,                    # 1=English, 2=French
    'ApplicationId': 37,               # Application ID
    'PropertySearchTypeId': 0,         # 0=No Preference
    'TransactionTypeId': 3,            # 3=For Rent, 2=For Sale
    'LatitudeMin': 45.247,            # Bounding box
    'LatitudeMax': 45.535,
    'LongitudeMin': -75.927,
    'LongitudeMax': -75.247,
    'PriceMin': 1000,                 # Optional
    'PriceMax': 2500,                 # Optional
    'Sort': '6-D',                    # Date posted (newest first)
    'RecordsPerPage': 50,             # Max results
    'PropertyTypeGroupID': 1          # 1=Residential
}
```

**Features:**
- ✅ Detailed property information (beds, baths, size)
- ✅ MLS numbers for unique identification
- ✅ High-quality photos
- ✅ Exact coordinates (latitude/longitude)
- ✅ Posted dates
- ✅ Property type classification

**Known Limitations:**
- Requires geographic coordinates (city must be in lookup table)
- API may return max 50 results per request
- Some listings may not have all fields populated

**Code Example:**
```python
from scrapers.realtor_ca_scraper import RealtorCAScraper

scraper = RealtorCAScraper()
listings = scraper.search(
    location='toronto',
    min_price=1500,
    max_price=3000
)

for listing in listings:
    print(f"{listing['title']} - ${listing['price']}/mo")
    print(f"  {listing['bedrooms']} bed, {listing['bathrooms']} bath")
    print(f"  {listing['square_feet']} sq ft")
```

---

## Adding New Scrapers

### Step 1: Create Scraper File

Create `scrapers/new_site_scraper.py`:

```python
"""
NewSite Scraper
Description of what this scraper does
"""

from typing import Any, Dict, List, Optional
from scrapers.base_scraper import BaseScraper

class NewSiteScraper(BaseScraper):
    """Scraper for NewSite.com rental listings"""
    
    def get_source_name(self) -> str:
        """Return the source identifier"""
        return "newsite"
    
    def build_search_url(
        self,
        location: str,
        min_price: Optional[int] = None,
        max_price: Optional[int] = None,
    ) -> str:
        """Build the search URL with parameters"""
        # Implement URL construction
        base_url = "https://www.newsite.com/search"
        # Add parameters
        return f"{base_url}?location={location}&min={min_price}&max={max_price}"
    
    def parse_listings(self, html: str) -> List[Dict[str, Any]]:
        """Parse HTML and extract listing data"""
        from bs4 import BeautifulSoup
        
        listings = []
        soup = BeautifulSoup(html, 'html.parser')
        
        # Find listing elements
        listing_cards = soup.find_all('div', class_='listing-card')
        
        for card in listing_cards:
            listing = {
                'id': card.get('data-id'),
                'title': card.find('h2').text.strip(),
                'price': card.find('span', class_='price').text,
                'location': card.find('span', class_='location').text,
                'url': card.find('a')['href'],
            }
            listings.append(listing)
        
        return listings
```

### Step 2: Test Your Scraper

Add test code at the bottom:

```python
if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.DEBUG)
    
    scraper = NewSiteScraper()
    results = scraper.search('ottawa', 1000, 2000)
    print(f"Found {len(results)} listings")
```

Run: `python scrapers/new_site_scraper.py`

### Step 3: Add to Test Suite

Update `test_scrapers.py` to include your new scraper.

### Best Practices

1. **Start Simple:** Get basic data first (title, price, URL)
2. **Add Incrementally:** Add more fields (beds, baths) later
3. **Handle Errors:** Wrap parsing in try/except blocks
4. **Log Everything:** Use `self.logger` for debugging
5. **Save Debug Data:** Enable `save_debug_html` during development
6. **Respect Robots.txt:** Check site's scraping policy
7. **Rate Limit:** Use `self._rate_limit()` before requests
8. **Test Thoroughly:** Try different cities and price ranges

### Common Patterns

**Pattern 1: HTML Parsing**
```python
def parse_listings(self, html: str) -> List[Dict]:
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    
    listings = []
    for card in soup.select('.listing-card'):
        listing = {
            'title': card.select_one('.title').text,
            'price': self._extract_price(card.select_one('.price').text),
            'url': card.select_one('a')['href']
        }
        listings.append(listing)
    return listings
```

**Pattern 2: JSON API**
```python
def search(self, location, min_price, max_price, **kwargs):
    # Override search to use POST with JSON
    url = self.build_search_url(location, min_price, max_price)
    payload = self._build_api_payload(location, min_price, max_price)
    
    response = self.session.post(url, json=payload)
    data = response.json()
    
    raw_listings = self._extract_from_json(data)
    return [self.standardize_listing(l) for l in raw_listings]
```

**Pattern 3: JavaScript-Rendered (Selenium)**
```python
from selenium import webdriver
from selenium.webdriver.common.by import By

def search(self, location, min_price, max_price, **kwargs):
    driver = webdriver.Chrome()
    driver.get(self.build_search_url(location, min_price, max_price))
    
    # Wait for content to load
    time.sleep(3)
    
    # Extract data
    listings = []
    cards = driver.find_elements(By.CLASS_NAME, 'listing-card')
    for card in cards:
        listing = {
            'title': card.find_element(By.CLASS_NAME, 'title').text,
            # ... extract more fields
        }
        listings.append(listing)
    
    driver.quit()
    return [self.standardize_listing(l) for l in listings]
```

---

## Troubleshooting

### Issue: No Listings Found

**Possible Causes:**
1. Website structure changed
2. Invalid location name
3. No listings match criteria
4. Anti-scraping measures (CAPTCHA, IP block)

**Solutions:**
```python
# Enable debug mode
scraper = KijijiScraper({'save_debug_html': True})
results = scraper.search('ottawa', 1000, 2000)

# Check debug_output/ folder for saved HTML/JSON
# Verify the website structure hasn't changed
```

### Issue: Import Errors

**Error:** `ModuleNotFoundError: No module named 'scrapers'`

**Solution:**
```bash
# Ensure you're in the project root
cd rental-scanner

# Install dependencies
pip install -r requirements.txt

# Run from project root
python test_scrapers.py
```

### Issue: Timeout Errors

**Error:** `requests.exceptions.Timeout`

**Solution:**
```python
# Increase timeout
scraper = KijijiScraper({'timeout': 60})  # 60 seconds

# Or retry
for attempt in range(3):
    try:
        results = scraper.search('ottawa', 1000, 2000)
        break
    except Exception as e:
        print(f"Attempt {attempt + 1} failed: {e}")
```

### Issue: Wrong Data Format

**Error:** Data doesn't match standardized format

**Solution:**
```python
# Check raw data first
raw = scraper.parse_listings(html)
print(raw[0])  # Inspect structure

# Then check standardization
standardized = scraper.standardize_listing(raw[0])
print(standardized)  # Verify format
```

### Issue: Rate Limiting

**Error:** Too many requests, getting blocked

**Solution:**
```python
# Increase delay between requests
scraper = KijijiScraper({'delay': 3})  # 3 seconds between requests

# Use rotating user agents
import random
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64)...',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...',
]
scraper.session.headers['User-Agent'] = random.choice(user_agents)
```

### Issue: CAPTCHA or Bot Detection

**Solutions:**
1. **Add delays:** Slow down requests to seem more human-like
2. **Rotate IPs:** Use proxy servers
3. **Use Selenium:** Render JavaScript like a real browser
4. **Look for APIs:** Official APIs are more reliable
5. **Respect robots.txt:** Check if scraping is allowed

### Common Debugging Commands

```bash
# Enable verbose logging
export LOG_LEVEL=DEBUG
python test_scrapers.py

# Test specific city
python -c "from scrapers.kijiji_scraper import KijijiScraper; \
           s = KijijiScraper(); \
           print(s.search('toronto', 1000, 2000))"

# Check saved debug files
ls -la debug_output/

# Verify HTML structure
python -c "from bs4 import BeautifulSoup; \
           html = open('debug_output/kijiji_*.html').read(); \
           soup = BeautifulSoup(html, 'html.parser'); \
           print(soup.prettify()[:1000])"
```

---

## API Reference

### BaseScraper Methods

**`get_source_name() -> str`**
- Returns source identifier (e.g., "kijiji")
- Must be implemented by subclasses

**`build_search_url(location, min_price, max_price) -> str`**
- Constructs search URL with parameters
- Must be implemented by subclasses

**`parse_listings(html) -> List[Dict]`**
- Extracts raw listing data from HTML
- Must be implemented by subclasses

**`search(location, min_price, max_price, **kwargs) -> List[Dict]`**
- Main entry point for searching
- Returns standardized listings
- Handles rate limiting, retries, filtering

**`standardize_listing(raw_listing) -> Dict`**
- Converts raw data to standard format
- Can be overridden for custom mapping

**`filter_results(listings, min_price, max_price) -> List[Dict]`**
- Filters listings by criteria
- Applied after standardization

### Configuration Options

Pass to scraper constructor:

```python
config = {
    'timeout': 30,              # Request timeout (seconds)
    'max_retries': 3,           # Number of retry attempts
    'delay': 1,                 # Delay between requests (seconds)
    'save_debug_html': False,   # Save responses for debugging
    'debug_output_dir': 'debug',# Debug file directory
    'user_agent': '...',        # Custom user agent string
}

scraper = KijijiScraper(config)
```

---

## Next Steps

1. **Test both scrapers:** Run `python test_scrapers.py`
2. **Review the code:** Check `scrapers/kijiji_scraper.py` and `scrapers/realtor_ca_scraper.py`
3. **Add more scrapers:** Follow the guide above for Rentals.ca, Viewit.ca, etc.
4. **Integrate with app:** Update `app.py` to use multiple scrapers
5. **Add to database:** Save results for tracking and history

---

## Resources

- **BeautifulSoup Docs:** https://www.crummy.com/software/BeautifulSoup/
- **Requests Docs:** https://requests.readthedocs.io/
- **Selenium Docs:** https://selenium-python.readthedocs.io/
- **Realtor.ca API:** https://github.com/Froren/realtorca
- **Web Scraping Best Practices:** https://www.scraperapi.com/blog/web-scraping-best-practices/

---

## Contributing

Found a bug? Have a new scraper? Contributions welcome!

1. Fork the repository
2. Create a feature branch
3. Add your scraper with tests
4. Submit a pull request

---

**Last Updated:** 2024-01-15  
**Version:** 2.0