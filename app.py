"""
rentFalcon Flask Application
Multi-source rental listing search powered by Scraper Manager
"""

import logging
from datetime import datetime

from flask import Flask, jsonify, render_template, request
from models.mongo_db import bulk_upsert_listings, get_all_active_listings, find_listings_near

from scrapers.scraper_manager import ScraperManager

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-secret-key-change-in-production"

# NOTE: MongoDB connection is initialized in models.mongo_db
# For a real app, you would ensure the connection is robustly handled here.

# Initialize Scraper Manager with configuration
# This runs once at startup
scraper_config = {
    "enabled_scrapers": [
        "kijiji",
        "rentals_ca",
    ],  # Working scrapers only (Realtor.ca disabled - returns 0 results)
    "max_workers": 3,
    "deduplicate": True,
    "similarity_threshold": 0.85,
    "timeout": 60,
    "scraper_configs": {
        "rentals_ca": {
            "use_selenium": True  # Enable Selenium for rentals_ca scraping
        },
        "realtor_ca": {
            "use_selenium": True  # Enable Selenium for realtor_ca scraping (fallback)
        },
    },
}

# Create manager instance (singleton)
manager = ScraperManager(scraper_config)
logger.info(
    f"Scraper Manager initialized with scrapers: {', '.join(manager.get_enabled_scrapers())}"
)


@app.route("/", methods=["GET", "POST"])
def index():
    """Main search page"""
    current_year = datetime.now().year

    if request.method == "POST":
        try:
            # Get form data
            price_min = request.form.get("price_min")
            price_max = request.form.get("price_max")
            location = request.form.get("location", "newmarket")

            # Convert prices to integers
            min_price = int(price_min) if price_min else None
            max_price = int(price_max) if price_max else None

            # Validate location
            if not location or location.strip() == "":
                return render_template(
                    "index.html",
                    results=None,
                    search_params=request.form,
                    error="Please enter a location",
                    current_year=current_year,
                    available_scrapers=manager.get_available_scrapers(),
                    enabled_scrapers=manager.get_enabled_scrapers(),
                )

            logger.info(
                f"Search request: location={location}, min={min_price}, max={max_price}"
            )

            # Execute multi-source search
            result = manager.search_all(location, min_price, max_price)

            # Extract data
            scraped_listings = result["listings"]
            stats = result["stats"]
            errors = result["errors"]

            logger.info(
                f"Search complete: {len(scraped_listings)} unique listings from "
                f"{stats['scrapers_succeeded']} sources in {stats['execution_time']:.2f}s"
            )

            # --- MongoDB Integration: Save scraped data ---
            if scraped_listings:
                upsert_count = bulk_upsert_listings(scraped_listings)
                logger.info(f"MongoDB upsert complete: {upsert_count} listings updated/inserted.")
            # --- End MongoDB Integration ---

            # Log any errors
            if errors:
                for scraper, error in errors.items():
                    logger.warning(f"Scraper {scraper} failed: {error}")

            # For now, we will still return the scraped listings directly,
            # but in a real implementation, we would query the DB for the final,
            # enriched, and deduplicated set.
            # Since the current manager.search_all already handles deduplication,
            # we will stick to returning the scraped list for minimal app.py change.
            listings_to_display = scraped_listings

            return render_template(
                "index.html",
                results=listings_to_display,
                stats=stats,
                errors=errors,
                search_params=request.form,
                current_year=current_year,
                available_scrapers=manager.get_available_scrapers(),
                enabled_scrapers=manager.get_enabled_scrapers(),
            )

        except ValueError as e:
            logger.error(f"Invalid input: {e}")
            return render_template(
                "index.html",
                results=None,
                search_params=request.form,
                error=f"Invalid price values: {str(e)}",
                current_year=current_year,
                available_scrapers=manager.get_available_scrapers(),
                enabled_scrapers=manager.get_enabled_scrapers(),
            )

        except Exception as e:
            logger.error(f"Search error: {e}", exc_info=True)
            return render_template(
                "index.html",
                results=None,
                search_params=request.form,
                error=f"An error occurred: {str(e)}",
                current_year=current_year,
                available_scrapers=manager.get_available_scrapers(),
                enabled_scrapers=manager.get_enabled_scrapers(),
            )

    # GET request - show empty form
    # On initial load, display all active listings from the database
    initial_listings = get_all_active_listings(limit=50)
    logger.info(f"Initial load: {len(initial_listings)} active listings from MongoDB.")

    return render_template(
        "index.html",
        results=initial_listings,
        search_params=request.args,
        current_year=current_year,
        available_scrapers=manager.get_available_scrapers(),
        enabled_scrapers=manager.get_enabled_scrapers(),
    )


@app.route("/api/search", methods=["POST"])
def api_search():
    """API endpoint for programmatic access"""
    try:
        data = request.get_json()

        location = data.get("location")
        min_price = data.get("min_price")
        max_price = data.get("max_price")

        if not location:
            return jsonify({"error": "Location is required"}), 400

        # Execute search
        result = manager.search_all(location, min_price, max_price)

        # --- MongoDB Integration: Save scraped data ---
        scraped_listings = result["listings"]
        if scraped_listings:
            bulk_upsert_listings(scraped_listings)
        # --- End MongoDB Integration ---

        # In a real API, we would query the DB, but for now, return the scraped result
        return jsonify(result), 200

    except Exception as e:
        logger.error(f"API search error: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@app.route("/api/sources", methods=["GET"])
def api_sources():
    """Get available and enabled scrapers"""
    return jsonify(
        {
            "available": manager.get_available_scrapers(),
            "enabled": manager.get_enabled_scrapers(),
        }
    ), 200


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for monitoring"""
    try:
        available = manager.get_available_scrapers()
        enabled = manager.get_enabled_scrapers()

        return jsonify(
            {
                "status": "healthy",
                "scrapers_available": len(available),
                "scrapers_enabled": len(enabled),
                "timestamp": datetime.utcnow().isoformat(),
            }
        ), 200

    except Exception as e:
        return jsonify(
            {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat(),
            }
        ), 500


@app.errorhandler(404)
def not_found(e):
    """404 error handler"""
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(e):
    """500 error handler"""
    logger.error(f"Internal error: {e}", exc_info=True)
    return render_template("500.html"), 500


@app.context_processor
def inject_globals():
    """Inject global variables into all templates"""
    return {
        "app_name": "rentFalcon",
        "app_version": "2.1",
        "current_year": datetime.now().year,
    }


if __name__ == "__main__":
    # Development server
    logger.info("Starting rentFalcon application...")
    logger.info(f"Enabled scrapers: {', '.join(manager.get_enabled_scrapers())}")

    # Run with debug mode
    # For production, use: gunicorn -w 4 -b 0.0.0.0:5000 app:app
    app.run(host="0.0.0.0", port=5000, debug=True)
