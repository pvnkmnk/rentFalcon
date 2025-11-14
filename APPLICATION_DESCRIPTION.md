# Rental Scanner Application Overview

## Description

The **rental-scanner** is a Python Flask web application that scrapes Kijiji (a Canadian classifieds website) for rental apartment listings based on user-specified search criteria.

## Architecture & Components

### 1. Flask Web Application (`app.py`)
- Serves as the main entry point running a web server on debug mode
- Provides a single route (`/`) that handles both GET and POST requests
- Collects user input (price range, location) via a web form
- Passes search parameters to the scraper and displays results

### 2. Web Scraper (`scrapers/kijiji_scraper.py`)
- **Target**: Kijiji rental listings (category 37 = apartments-condos)
- **Method**: 
  - Constructs URLs like `https://www.kijiji.ca/b-apartments-condos/{location}/k0c37`
  - Uses `requests` library with custom User-Agent headers to fetch pages
  - Parses HTML with BeautifulSoup4 to extract JSON-LD structured data
- **Data Extraction**: Looks for `<script type="application/ld+json">` tags containing structured listing data (ItemList format)
- **Filters**: Applies client-side price filtering to match user criteria
- **Output**: Returns list of dictionaries with title, price, location, URL, description, and source

### 3. Dependencies (`requirements.txt`)
- **Flask**: Web framework
- **requests**: HTTP library for web scraping
- **beautifulsoup4**: HTML parsing
- **APScheduler**: For planned scheduled scanning feature (not yet implemented)

### 4. Search Parameters
- **Price Range**: Minimum and maximum monthly rent
- **Location**: City/area name (converted to URL-friendly slug like "ottawa" → "ottawa")
- Handles invalid inputs gracefully with type conversion and error handling

### 5. Data Flow
1. User submits form with search criteria
2. Flask app calls `scrape_kijiji()` with parameters
3. Scraper constructs Kijiji search URL with location and price filters
4. Fetches and parses HTML response
5. Extracts listing data from JSON-LD structured data
6. Filters results by price range
7. Returns up to 25 listings
8. Flask renders results in HTML template with search parameters preserved

### 6. Debugging Features
- Saves fetched HTML to `kijiji_debug_page.html` for troubleshooting
- Extensive console logging for request URLs, params, and parsing steps
- Error handling for network issues and parsing failures

## Planned Features
(Not yet implemented)
- Scheduled automated scans
- Tracking of removed/expired listings
- Report generation

## Setup Instructions

1. Create a Python virtual environment: `python -m venv venv`
2. Activate the virtual environment: 
   - Windows: `venv\Scripts\activate`
   - Linux/macOS: `source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Run the application: `python app.py`
5. Access the web interface at `http://localhost:5000`

## Use Case

The application is designed for local development use to help users find rental properties on Kijiji matching their budget and location preferences.
