# Newmarket Configuration Guide

## Overview

This document describes the configuration changes made to optimize the Rental Scanner for searching properties in and around Newmarket, Ontario, with a focus on the 25 km radius area.

## Changes Made

### 1. Default Location Updated

The default search location has been changed from **Ottawa** to **Newmarket, Ontario**.

**Files Modified:**
- `app.py` - Line 55: Default location parameter
- `templates/index.html` - Line 239: Default input value and placeholder text

### 2. Scrapers Enabled

All three scrapers are now enabled by default:

- ✅ **Kijiji** - Canada's largest classifieds site
- ✅ **Realtor.ca** - Official real estate listings
- ✅ **Rentals.ca** - Dedicated rental platform

**Files Modified:**
- `app.py` - Line 26: Added `"rentals_ca"` to enabled scrapers list
- `app.py` - Line 33: Enabled Selenium for rentals_ca scraper
- `scrapers/rentals_ca_scraper.py` - Updated to use webdriver-manager for automatic ChromeDriver installation

### 3. City Coverage

The following cities within 25 km of Newmarket are now explicitly supported in the Rentals.ca scraper:

| City | Distance from Newmarket | Province |
|------|-------------------------|----------|
| Newmarket | 0 km (center) | ON |
| Aurora | ~8 km south | ON |
| Richmond Hill | ~12 km south | ON |
| East Gwillimbury | ~15 km north | ON |
| Bradford | ~20 km northwest | ON |
| Markham | ~18 km southeast | ON |
| Vaughan | ~20 km southwest | ON |
| King City | ~10 km west | ON |

**Files Modified:**
- `scrapers/rentals_ca_scraper.py` - Lines 51-58: Added city slugs for Newmarket area
- `scrapers/realtor_ca_scraper.py` - Lines 43-51: Added coordinate boundaries for Newmarket area cities

### 4. User Interface Updates

The search form now includes helpful suggestions for nearby cities:

**Old placeholder:** "e.g., Ottawa, Toronto, Montreal"  
**New placeholder:** "e.g., Newmarket, Aurora, Richmond Hill, Bradford"

**Old help text:** "Enter a Canadian city name"  
**New help text:** "Enter Newmarket or nearby cities (Aurora, East Gwillimbury, Bradford, Richmond Hill, Markham, Vaughan, King City)"

## How to Use

### Basic Search

1. The location field now defaults to "Newmarket"
2. Simply enter your desired price range and click "Search Rentals"
3. Results will be aggregated from all three sources

### Searching Nearby Cities

To search in nearby cities, simply type any of these supported locations:
- Newmarket
- Aurora
- Richmond Hill
- East Gwillimbury
- Bradford
- Markham
- Vaughan
- King City

### Search Tips

1. **Broaden your search**: Try searching multiple cities to see more listings
2. **Price ranges**: Use realistic price ranges for the area (e.g., $1500-$2500 for 1-2 bedroom)
3. **Refresh frequency**: Listings are scraped in real-time, so you can search as often as needed
4. **Three sources**: The app combines results from Kijiji, Realtor.ca, and Rentals.ca for comprehensive coverage

## Technical Details

### Scraper Configuration

```json
{
  "enabled_scrapers": ["kijiji", "realtor_ca", "rentals_ca"],
  "max_workers": 3,
  "deduplicate": true,
  "similarity_threshold": 0.85,
  "timeout": 60,
  "scraper_configs": {
    "rentals_ca": {
      "use_selenium": true
    }
  }
}
```

### Selenium Setup

**Rentals.ca requires Selenium** for scraping because the site uses JavaScript to render content.

**Automatic ChromeDriver Management:**
- The app uses `webdriver-manager` to automatically download and manage ChromeDriver
- No manual ChromeDriver installation needed
- Chrome browser must be installed on your system
- First run will download ChromeDriver (one-time setup)

**Dependencies Installed:**
- `selenium` - Web browser automation
- `webdriver-manager` - Automatic ChromeDriver management

**How It Works:**
1. When searching, Rentals.ca scraper launches a headless Chrome browser
2. Chrome loads the search page and executes JavaScript
3. Scraper extracts rendered HTML with listings
4. Browser closes automatically
5. ChromeDriver is cached for future searches

### Deduplication

The system automatically removes duplicate listings that appear on multiple sites using:
- Title similarity matching (85% threshold)
- Address comparison
- Price matching

### Performance

- **Parallel execution**: All scrapers run simultaneously
- **Response time**: Typically 5-15 seconds for complete results
- **Max timeout**: 60 seconds per search

## Troubleshooting

### Chrome/ChromeDriver Issues

If you get Selenium or ChromeDriver errors:

1. **Install Chrome**: Make sure Google Chrome is installed on your system
2. **First run delay**: First search may take 30-60 seconds while ChromeDriver downloads
3. **Clear cache**: Delete the `.wdm` folder in your user directory if issues persist
4. **Manual install**: If auto-install fails, install ChromeDriver manually

### No Results Found

If you're not seeing results:

1. **Check spelling**: Ensure city names are spelled correctly
2. **Try nearby cities**: Some sites may have more listings for larger cities
3. **Adjust price range**: Try widening your price range
4. **Check logs**: Look at the console output for any scraper errors
5. **Wait for Selenium**: Rentals.ca scraping takes longer (uses browser automation)

### Slow Response Time

If searches are taking too long:

1. The first search may take longer (10-15 seconds)
2. Subsequent searches should be faster
3. Check your internet connection
4. Some sites may be slow to respond

### Missing Rentals.ca Results

If Rentals.ca isn't returning results:

1. Verify the city is in the supported list above
2. Check if the site is accessible in your browser
3. Ensure Chrome browser is installed
4. Check console for Selenium errors
5. First search may take longer (ChromeDriver download)
6. Rentals.ca searches typically take 10-20 seconds due to browser automation

## System Requirements

### Required Software
- **Python 3.8+** (tested with Python 3.13)
- **Google Chrome** (latest version recommended)
- **Internet connection** (for scraping and ChromeDriver download)

### Required Python Packages
- Flask, Flask-SQLAlchemy - Web framework
- requests, beautifulsoup4 - Web scraping
- selenium - Browser automation (for Rentals.ca)
- webdriver-manager - Automatic ChromeDriver management
- APScheduler - Task scheduling
- python-dotenv - Environment configuration

### Optional
- ChromeDriver (auto-installed by webdriver-manager)

## Future Enhancements

Potential improvements for Newmarket area searches:

- [ ] Add support for more local listing sites
- [ ] Implement saved searches for Newmarket area
- [ ] Add email alerts for new Newmarket listings
- [ ] Create custom filters for Newmarket neighborhoods
- [ ] Add map view centered on Newmarket
- [ ] Optimize Selenium performance (faster page loads)

## Support

For issues or questions:
1. Check the main README.md
2. Review the SCRAPER_GUIDE.md
3. Check application logs in `rental_scanner.log`

## Configuration Files

Key files for Newmarket configuration:
- `app.py` - Main application and default settings
- `config.py` - Global configuration
- `scrapers/rentals_ca_scraper.py` - City mappings
- `templates/index.html` - User interface

---

**Last Updated**: January 2025  
**Configuration Version**: 2.1 (Newmarket Edition)