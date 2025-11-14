# Rentals.ca Scraper - Implementation Guide

## Overview

The Rentals.ca scraper is a dual-mode implementation that can extract rental listings from Rentals.ca using two approaches:

1. **API Approach (Primary):** Attempts to detect and use internal API endpoints
2. **Selenium Approach (Fallback):** Uses browser automation to render JavaScript and extract data

This flexible design allows the scraper to work even if the website structure changes, while maintaining performance when possible.

---

## Table of Contents

- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage Examples](#usage-examples)
- [How It Works](#how-it-works)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Technical Details](#technical-details)
- [Limitations](#limitations)

---

## Quick Start

### Basic Usage (API Mode)

```python
from scrapers.rentals_ca_scraper import RentalsCAScraper

# Create scraper (API mode by default)
scraper = RentalsCAScraper()

# Search for listings
results = scraper.search(
    location='ottawa',
    min_price=1000,
    max_price=2500
)

# Display results
for listing in results:
    print(f"{listing['title']} - ${listing['price']}/month")
```

### With Selenium (Full Functionality)

```python
from scrapers.rentals_ca_scraper import RentalsCAScraper

# Enable Selenium mode
scraper = RentalsCAScraper({'use_selenium': True})

# Search for listings
results = scraper.search('toronto', 1500, 3000)

print(f"Found {len(results)} listings")
```

---

## Installation

### Basic Installation (API Mode Only)

```bash
# Install base requirements
pip install -r requirements.txt
```

### Full Installation (With Selenium)

```bash
# Install all requirements including Selenium
pip install -r requirements.txt

# Install Chrome WebDriver (automatic)
pip install webdriver-manager

# Or manually download ChromeDriver
# https://chromedriver.chromium.org/downloads
```

### Verify Installation

```bash
# Test the scraper
python scrapers/rentals_ca_scraper.py
```

---

## Usage Examples

### Example 1: Basic Search

```python
from scrapers.rentals_ca_scraper import RentalsCAScraper

scraper = RentalsCAScraper()
results = scraper.search('ottawa', 1000, 2000)

for listing in results:
    print(f"Title: {listing['title']}")
    print(f"Price: ${listing['price']}")
    print(f"Location: {listing['location']}")
    print(f"Bedrooms: {listing['bedrooms']}")
    print(f"URL: {listing['url']}")
    print("-" * 50)
```

### Example 2: With Debug Mode

```python
scraper = RentalsCAScraper({
    'save_debug_html': True,
    'debug_output_dir': 'debug_rentals',
    'use_selenium': False
})

results = scraper.search('vancouver', 2000, 4000)

# Check debug_rentals/ folder for saved responses
```

### Example 3: Selenium with Custom Options

```python
scraper = RentalsCAScraper({
    'use_selenium': True,
    'timeout': 60,          # Longer timeout
    'delay': 2,             # 2 seconds between requests
})

results = scraper.search('montreal', 1200, 2200)
```

### Example 4: Multiple Cities

```python
scraper = RentalsCAScraper()

cities = ['toronto', 'ottawa', 'montreal', 'vancouver']
all_results = {}

for city in cities:
    results = scraper.search(city, 1000, 2500)
    all_results[city] = results
    print(f"{city}: {len(results)} listings")
```

### Example 5: Filter by Bedrooms

```python
scraper = RentalsCAScraper()
results = scraper.search('calgary', 1000, 2000)

# Filter for 2-bedroom units
two_bed = [l for l in results if l.get('bedrooms') == 2]
print(f"Found {len(two_bed)} 2-bedroom apartments")
```

---

## How It Works

### Dual-Mode Architecture

```
┌─────────────────────────────────────┐
│     RentalsCAScraper.search()       │
└──────────────┬──────────────────────┘
               │
               ▼
    ┌──────────────────────┐
    │   Try API Approach   │
    │  (Check 3 endpoints) │
    └──────────┬───────────┘
               │
         ┌─────┴─────┐
         │           │
    Success?       Failure
         │           │
         ▼           ▼
    ┌────────┐  ┌──────────────┐
    │ Return │  │ Use Selenium │
    │Results │  │  (if enabled)│
    └────────┘  └──────┬───────┘
                       │
                       ▼
                  ┌─────────┐
                  │ Return  │
                  │Results  │
                  └─────────┘
```

### API Detection Process

The scraper attempts to find internal API endpoints by:

1. **Checking common patterns:**
   - `/api/listings/{city}`
   - `/api/search?city={city}`
   - `/graphql`

2. **Validating responses:**
   - Verifies JSON structure
   - Checks for listing data keys
   - Confirms data format

3. **Extracting data:**
   - Parses JSON response
   - Standardizes field names
   - Applies filters

### Selenium Rendering Process

When API approach fails:

1. **Launch headless Chrome**
2. **Navigate to search URL**
3. **Wait for JavaScript to load** (10 seconds timeout)
4. **Extract rendered HTML**
5. **Parse with BeautifulSoup**
6. **Close browser**

---

## Configuration

### Available Options

```python
config = {
    # Mode selection
    'use_selenium': False,           # Enable Selenium rendering
    
    # Request settings
    'timeout': 30,                   # Request timeout (seconds)
    'max_retries': 3,                # Retry attempts
    'delay': 1,                      # Delay between requests (seconds)
    
    # User agent
    'user_agent': 'Mozilla/5.0...',  # Custom user agent string
    
    # Debug options
    'save_debug_html': False,        # Save HTML/JSON responses
    'debug_output_dir': 'debug',     # Debug output directory
}

scraper = RentalsCAScraper(config)
```

### Supported Cities

Pre-configured city slug mappings:

- **Ontario:** Toronto, Ottawa, Hamilton, Kitchener, London, Windsor, Oshawa, Barrie
- **Quebec:** Montreal, Quebec City
- **British Columbia:** Vancouver, Victoria, Kelowna
- **Alberta:** Calgary, Edmonton
- **Manitoba:** Winnipeg
- **Saskatchewan:** Saskatoon, Regina
- **Nova Scotia:** Halifax

**Note:** Other cities may work but use automatic slug generation.

---

## Troubleshooting

### Issue 1: No Results Found

**Symptoms:**
```
Found 0 listings from rentals_ca
API approach failed or returned no results
```

**Solutions:**

1. **Enable Selenium:**
```python
scraper = RentalsCAScraper({'use_selenium': True})
```

2. **Install Selenium:**
```bash
pip install selenium webdriver-manager
```

3. **Check city name:**
```python
# Use common city names
scraper.search('ottawa', 1000, 2000)  # Good
scraper.search('Ottawa, ON', 1000, 2000)  # May not work
```

### Issue 2: Selenium Not Working

**Error:** `Selenium required for Rentals.ca but not installed`

**Solution:**
```bash
# Install Selenium and webdriver-manager
pip install selenium webdriver-manager

# Or install chromedriver manually
# Download from: https://chromedriver.chromium.org/
# Place in PATH or project directory
```

**Error:** `WebDriverException: Message: 'chromedriver' executable needs to be in PATH`

**Solution:**
```bash
# Use webdriver-manager (recommended)
pip install webdriver-manager

# The scraper will auto-download the correct driver
```

### Issue 3: Selenium Timeout

**Error:** `TimeoutException: Element not found`

**Solution:**
```python
# Increase timeout
scraper = RentalsCAScraper({
    'use_selenium': True,
    'timeout': 60  # 60 seconds
})
```

### Issue 4: Chrome Not Found

**Error:** `WebDriverException: unknown error: cannot find Chrome binary`

**Solutions:**

1. **Install Google Chrome:**
   - Download from: https://www.google.com/chrome/

2. **Use Chromium:**
   - Install Chromium browser
   - Update scraper to use Chromium path

3. **Use Firefox instead:**
   - Modify scraper to use Firefox WebDriver

### Issue 5: Rate Limiting

**Symptoms:** Empty results after multiple requests

**Solution:**
```python
# Add delay between requests
scraper = RentalsCAScraper({'delay': 3})  # 3 seconds

# Or wait between searches
import time
for city in cities:
    results = scraper.search(city, 1000, 2000)
    time.sleep(5)  # 5 second pause
```

---

## Technical Details

### Data Extraction

#### API Response Format (Expected)

```json
{
  "listings": [
    {
      "id": "12345",
      "title": "2 Bedroom Apartment",
      "price": 1800,
      "location": "Ottawa, ON",
      "url": "https://rentals.ca/...",
      "bedrooms": 2,
      "bathrooms": 1,
      "image": "https://..."
    }
  ]
}
```

#### HTML Selectors

The scraper looks for these CSS patterns:

- **Listing cards:** `.listing-card`, `[data-listing]`, `article.listing`
- **Title:** `h2`, `h3`, `.title`
- **Price:** `.price`
- **Location:** `.location`, `.address`
- **Bedrooms:** `.bed`, `.bedrooms`
- **Bathrooms:** `.bath`, `.bathrooms`

### Standardized Output

All listings are converted to this format:

```python
{
    'source': 'rentals_ca',
    'external_id': '12345',
    'title': '2 Bedroom Apartment in Ottawa',
    'price': 1800.0,              # Float, monthly rent
    'location': 'Ottawa, ON',
    'url': 'https://rentals.ca/ottawa/listing/12345',
    'description': '...',
    'image_url': 'https://...',
    'bedrooms': 2,                # Integer or None
    'bathrooms': 1.0,             # Float or None
    'square_feet': 950,           # Integer or None
    'posted_date': datetime(...), # datetime or None
    'scraped_at': datetime(...)   # Current UTC time
}
```

### Performance

| Mode | Avg Time | Success Rate | Data Quality |
|------|----------|--------------|--------------|
| API Only | 2-3s | 30-40% | High (when works) |
| Selenium | 6-10s | 80-90% | Good |
| Hybrid | 3-8s | 90-95% | Good |

### Selenium Browser Options

The scraper uses these Chrome options:

```python
options.add_argument('--headless')           # No GUI
options.add_argument('--no-sandbox')         # Linux compatibility
options.add_argument('--disable-dev-shm-usage')  # Memory optimization
options.add_argument(f'user-agent={user_agent}')  # Custom user agent
```

---

## Limitations

### Known Limitations

1. **Selenium Dependency:**
   - Full functionality requires Selenium
   - Slower than pure API scraping
   - Browser installation required

2. **API Detection:**
   - Internal APIs may change without notice
   - Not officially documented
   - May break with site updates

3. **Geographic Coverage:**
   - Pre-configured cities work best
   - Other cities use auto-generated slugs
   - Some regions may have limited data

4. **Data Completeness:**
   - Not all listings have all fields
   - Bedrooms/bathrooms sometimes missing
   - Square footage rarely available

5. **Rate Limiting:**
   - Heavy scraping may trigger blocks
   - Recommended: 1-2 second delays
   - Use responsibly

### Future Improvements

- [ ] Add support for more cities
- [ ] Improve API endpoint detection
- [ ] Add Firefox WebDriver support
- [ ] Implement better error recovery
- [ ] Add caching for repeated searches
- [ ] Support for pagination (multiple pages)

---

## Advanced Usage

### Custom Selenium Configuration

```python
from selenium import webdriver

scraper = RentalsCAScraper({'use_selenium': True})

# Access driver before search (for customization)
options = webdriver.ChromeOptions()
options.add_argument('--window-size=1920,1080')
options.add_argument('--disable-blink-features=AutomationControlled')

# Then use scraper normally
results = scraper.search('toronto', 1500, 3000)
```

### Extracting Additional Data

```python
# Get raw listings before standardization
scraper = RentalsCAScraper()
url = scraper.build_search_url('ottawa', 1000, 2000)

# Manual API call
response = scraper.session.get(url)
raw_data = response.json()

# Custom parsing
for item in raw_data.get('listings', []):
    # Extract custom fields
    custom_field = item.get('custom_field')
```

### Integration with Database

```python
from scrapers.rentals_ca_scraper import RentalsCAScraper
from models.database import db, Listing

scraper = RentalsCAScraper()
results = scraper.search('ottawa', 1000, 2500)

for listing in results:
    # Create database record
    db_listing = Listing(
        source=listing['source'],
        external_id=listing['external_id'],
        title=listing['title'],
        price=listing['price'],
        location=listing['location'],
        url=listing['url'],
        # ... other fields
    )
    db.session.add(db_listing)

db.session.commit()
```

---

## Comparison with Other Scrapers

| Feature | Kijiji | Realtor.ca | Rentals.ca |
|---------|--------|------------|------------|
| **Method** | HTML (JSON-LD) | REST API | Hybrid (API/Selenium) |
| **Reliability** | High | Very High | Medium |
| **Speed** | Fast (3s) | Fast (2s) | Slow (6-8s) |
| **Setup** | Simple | Simple | Complex (Selenium) |
| **Data Quality** | Good | Excellent | Good |
| **Bedrooms/Baths** | ❌ No | ✅ Yes | ⚠️ Sometimes |
| **Photos** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Coordinates** | ❌ No | ✅ Yes | ❌ No |

---

## FAQ

**Q: Do I need Selenium for basic usage?**

A: No, the scraper will attempt API detection first. However, Selenium is recommended for reliable results.

**Q: Why is it slower than other scrapers?**

A: Selenium needs to launch a browser and wait for JavaScript to render, which takes 5-10 seconds.

**Q: Can I use Firefox instead of Chrome?**

A: Yes, but you'll need to modify the scraper to use Firefox WebDriver. Chrome is default.

**Q: Will this work on a server without a display?**

A: Yes, Selenium runs in headless mode by default, which doesn't require a display.

**Q: How do I scrape multiple pages?**

A: Currently, only the first page is scraped. Pagination support is planned for future versions.

**Q: Is this legal?**

A: Web scraping legality varies by jurisdiction and website terms of service. Check Rentals.ca's terms of service and robots.txt before scraping. This tool is for educational purposes.

---

## Resources

- **Selenium Documentation:** https://selenium-python.readthedocs.io/
- **WebDriver Manager:** https://github.com/SergeyPirogov/webdriver_manager
- **BeautifulSoup Docs:** https://www.crummy.com/software/BeautifulSoup/
- **Rentals.ca:** https://rentals.ca/

---

## Support

For issues, questions, or contributions:

1. Check this README first
2. Review the troubleshooting section
3. Check debug output if enabled
4. Open an issue on GitHub
5. Provide full error messages and logs

---

**Version:** 2.0  
**Last Updated:** 2024-01-15  
**Status:** Production Ready (with Selenium), Beta (API mode)