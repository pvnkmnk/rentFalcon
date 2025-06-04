import requests
from bs4 import BeautifulSoup
import json
import os
import sys

# Add project root to sys.path to allow direct execution of this script for testing
# and correct relative imports if this module is imported elsewhere.
# This is more robust for different execution contexts.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

# Placeholder for Kijiji base URL and parameters
KIJIJI_BASE_URL = "https://www.kijiji.ca/b-apartments-condos/"

def scrape_kijiji(price_min=None, price_max=None, location=None):
    # Ensure price_min and price_max are integers if they are provided and convertible
    if price_min is not None:
        try:
            price_min = int(price_min)
        except (ValueError, TypeError):
            print(f"Warning: Invalid value for price_min '{price_min}', ignoring.")
            price_min = None
    if price_max is not None:
        try:
            price_max = int(price_max)
        except (ValueError, TypeError):
            print(f"Warning: Invalid value for price_max '{price_max}', ignoring.")
            price_max = None

    """Scrapes Kijiji for rental listings based on parameters."""
    listings = []
    
    # Sanitize location for URL (e.g., 'City Of Toronto' -> 'city-of-toronto')
    # Kijiji uses specific location slugs. A more robust solution would map user input to these slugs.
    # For now, a simple replacement and lowercasing.
    if location:
        location_slug = location.lower().replace(' ', '-').replace('_', '-')
    else:
        # Default to a broad area if no location is specified, though Kijiji usually requires one.
        # This might need to be a specific known slug like 'gta-greater-toronto-area' or similar.
        location_slug = 'canada' # A very broad default, likely needs refinement or make location mandatory

    # Construct the search URL
    # Kijiji URL structure: /b-apartments-condos/{location_slug}/c37l{location_id}
    # c37 is categoryId for 'apartments-condos'.
    # We'll use k0 for 'all of location' if no specific location_id is available, and c37 for category.
    # Example: /ottawa-gatineau-area/c37l1700184 or /ottawa/k0c37
    # For now, we'll try a common pattern: {location_slug}/k0c37 (all of the location for category 37)
    # This might be less precise than a URL with a specific location_id (e.g., l1700274)
    search_url = f"{KIJIJI_BASE_URL}{location_slug}/k0c37" 

    params = {}
    price_filter_parts = []
    if price_min:
        price_filter_parts.append(str(price_min))
    else:
        price_filter_parts.append('') # Kijiji uses '__' for one-sided ranges, e.g., '1000__' or '__2000'
    
    if price_max:
        price_filter_parts.append(str(price_max))
    else:
        price_filter_parts.append('')

    if price_min or price_max:
        params['price'] = '__'.join(price_filter_parts)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    print(f"Scraping URL: {search_url} with params: {params}") # Debug print

    try:
        response = requests.get(search_url, params=params, headers=headers, timeout=15)
        response.raise_for_status()

        # --- Save HTML content for debugging ---
        try:
            with open("kijiji_debug_page.html", "w", encoding='utf-8') as f_debug:
                f_debug.write(response.text)
            print("DEBUG: Saved Kijiji HTML to kijiji_debug_page.html")
        except Exception as e_write:
            print(f"DEBUG: Error writing debug HTML file: {e_write}")
        # --- End save HTML content ---

        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Attempt to find JSON-LD script tag containing structured data
        json_ld_script = soup.find('script', type='application/ld+json')
        
        if json_ld_script:
            print("Found JSON-LD script tag. Attempting to parse structured data.")
            try:
                data = json.loads(json_ld_script.string)
                if data and data.get('@type') == 'ItemList' and 'itemListElement' in data:
                    MAX_LISTINGS = 25
                    for item_entry in data['itemListElement']:
                        if len(listings) >= MAX_LISTINGS:
                            break
                        
                        item_details = item_entry.get('item', {})
                        if not item_details or item_details.get('@type') not in ['SingleFamilyResidence', 'Apartment', 'Residence', 'House']:
                            # Add more types if Kijiji uses others for rentals
                            continue

                        title_text = item_details.get('name', 'N/A')
                        ad_url = item_details.get('url', '#')
                        description_text = item_details.get('description', 'N/A')
                        
                        price_text = 'N/A'
                        offers = item_details.get('offers', {})
                        if isinstance(offers, list): # Sometimes offers can be a list
                            if offers:
                                offers = offers[0] # Take the first offer
                        if isinstance(offers, dict) and offers.get('@type') == 'Offer':
                            price_value = offers.get('price')
                            price_currency = offers.get('priceCurrency')
                            if price_value is not None:
                                price_text = f"{price_currency} {price_value}" if price_currency else str(price_value)
                        
                        location_text = 'N/A'
                        address_info = item_details.get('address')
                        if isinstance(address_info, str):
                            location_text = address_info
                        elif isinstance(address_info, dict):
                            # Construct address string from parts if available
                            parts = [address_info.get('streetAddress'), 
                                     address_info.get('addressLocality'), 
                                     address_info.get('addressRegion'), 
                                     address_info.get('postalCode')]
                            location_text = ', '.join(filter(None, parts))
                            if not location_text: # Fallback if parts are empty
                                location_text = str(address_info) # Or just use the dict as string

                        # Basic price filtering (if provided)
                        price_ok = True
                        if price_min is not None or price_max is not None:
                            try:
                                # Extract numeric part of price for comparison
                                current_price_str = ''.join(filter(str.isdigit, str(offers.get('price', ''))))
                                if current_price_str:
                                    current_price = int(current_price_str)
                                    if price_min is not None and current_price < price_min:
                                        price_ok = False
                                    if price_max is not None and current_price > price_max:
                                        price_ok = False
                                elif price_text != 'N/A': # If price_text is not 'N/A' but couldn't be parsed as int
                                    price_ok = False
                            except ValueError:
                                price_ok = False
                        
                        if price_ok and title_text != 'N/A' and ad_url != '#':
                            listings.append({
                                'title': title_text,
                                'price': price_text,
                                'location': location_text,
                                'url': ad_url,
                                'description': description_text,
                                'source': 'Kijiji'
                            })
                else:
                    print("JSON-LD data found, but not in expected ItemList format.")
            except json.JSONDecodeError as e_json:
                print(f"Error decoding JSON-LD: {e_json}")
            except Exception as e_parse:
                print(f"Error parsing JSON-LD content: {e_parse}")
        else:
            print("JSON-LD script tag not found. The page structure might have changed or it's not present for this query.")

        if not listings:
            print("No listings extracted. Check debug messages above.")
            return [{'title': 'No listings found', 'price': '', 'location': '', 'url': '#', 'description': 'Could not extract listings. Kijiji structure may have changed or no ads match.'}]

    except requests.exceptions.RequestException as e:
        print(f"Error fetching Kijiji page: {e}")
        # Also save HTML on request error if response object exists and has content
        if 'response' in locals() and response is not None and hasattr(response, 'text') and response.text:
            try:
                with open("kijiji_error_page.html", "w", encoding='utf-8') as f_debug_err:
                    f_debug_err.write(response.text)
                print("DEBUG: Saved Kijiji HTML (on error) to kijiji_error_page.html")
            except Exception as e_write_err:
                print(f"DEBUG: Error writing debug HTML file on request error: {e_write_err}")
        return [{'title': 'Error fetching Kijiji', 'price': '', 'location': '', 'url': '#', 'description': str(e)}]
    except Exception as e:
        print(f"An error occurred during scraping: {e}")
        import traceback
        traceback.print_exc()
        return [{'title': 'Scraping Error', 'price': '', 'location': '', 'url': '#', 'description': str(e)}]

    # This block should be at the same indentation level as the try/except
    if not listings: # Changed from elif to if, as it's a final check after try/except
        listings.append({'title': 'No listings found.', 'price': '', 'location': '', 'url': '#', 'description': 'Verify search terms or Kijiji might have blocked the request. Try a different User-Agent or check URL.'})

    return listings

if __name__ == '__main__':
    print("Testing Kijiji Scraper directly...")
    # Test with a common location like 'ottawa-gatineau-area' or 'gta-greater-toronto-area' (Kijiji slugs)
    # Or a city name like 'ottawa'
    test_location = 'ottawa'
    print(f"Searching for listings in: {test_location}")
    test_results = scrape_kijiji(price_min='1000', price_max='2500', location=test_location)
    
    if test_results:
        print(f"Found {len(test_results)} results:")
        for i, res in enumerate(test_results):
            print(f"--- Result {i+1} ---")
            print(f"  Title: {res['title']}")
            print(f"  Price: {res['price']}")
            print(f"  Location: {res['location']}")
            print(f"  URL: {res['url']}")
            print(f"  Desc: {res.get('description', 'N/A')[:100]}...")
            print("")
    else:
        print("No results returned from test scrape or an error occurred.")
