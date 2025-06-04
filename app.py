from flask import Flask, render_template, request
from scrapers import scrape_kijiji # Corrected import
import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Process form data here
        price_min = request.form.get('price_min')
        price_max = request.form.get('price_max')
        location = request.form.get('location')
        # Call scraper function and pass parameters
        print(f"Form data: Min Price: {price_min}, Max Price: {price_max}, Location: {location}") # Debug print
        results = scrape_kijiji(price_min=price_min, price_max=price_max, location=location)
        print(f"Scraper returned {len(results)} results.") # Debug print
        current_year = datetime.datetime.now().year
        return render_template('index.html', results=results, search_params=request.form, current_year=current_year)
    # For GET requests, pass empty search_params or load from session/cookies if implementing persistence
    current_year = datetime.datetime.now().year
    return render_template('index.html', results=None, search_params=request.args, current_year=current_year) # Pass args for potential pre-filled links

if __name__ == '__main__':
    app.run(debug=True)
