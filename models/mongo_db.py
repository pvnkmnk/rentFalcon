import os
from datetime import datetime, timedelta
from typing import List, Dict, Any

from pymongo import MongoClient
from pymongo.errors import ConnectionError, OperationFailure

# --- Configuration ---
# In a real application, this would be loaded from config.py or environment variables
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME", "rentFalcon")
LISTINGS_COLLECTION = "listings"

# --- Connection Setup ---
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client[MONGO_DB_NAME]
    listings_collection = db[LISTINGS_COLLECTION]
    client.admin.command('ping') # The ping command is cheap and does not require auth.
    print("Successfully connected to MongoDB.")
except ConnectionError as e:
    print(f"Could not connect to MongoDB: {e}")
    # Fallback or exit strategy would be here in a real app
    client = None
    db = None
    listings_collection = None

# --- Core Functions Implementation (Path 3) ---

def setup_mongo_indexes():
    """
    Sets up necessary indexes, including the TTL index and the 2dsphere index for GeoJSON.
    """
    if listings_collection is None:
        return

    # 1. TTL Indexing for Expiration (Path 3, Feature 2)
    # Listings older than 30 days since last_seen will be automatically removed by MongoDB
    # This simplifies cleanup logic in the application.
    try:
        listings_collection.create_index(
            "last_seen",
            expireAfterSeconds=int(timedelta(days=30).total_seconds()),
            name="ttl_last_seen_index"
        )
        print("TTL index created on 'last_seen'.")
    except OperationFailure as e:
        print(f"Failed to create TTL index: {e}")

    # 2. GeoJSON Querying Index (Path 3, Feature 3)
    # Index for fast geospatial queries
    try:
        listings_collection.create_index(
            [("location.coordinates", "2dsphere")],
            name="geojson_2dsphere_index"
        )
        print("2dsphere index created on 'location.coordinates'.")
    except OperationFailure as e:
        print(f"Failed to create 2dsphere index: {e}")

    # 3. Unique Index for Upsert
    # Ensures no duplicate listings based on source and external_id
    try:
        listings_collection.create_index(
            [("source", 1), ("external_id", 1)],
            unique=True,
            name="unique_source_external_id"
        )
        print("Unique index created on 'source' and 'external_id'.")
    except OperationFailure as e:
        print(f"Failed to create unique index: {e}")


def upsert_listing_document(listing_data: Dict[str, Any]) -> bool:
    """
    Dynamic Schema Upsert (Path 3, Feature 1)
    Inserts a new listing or updates an existing one based on source and external_id.
    Handles dynamic fields from different scrapers.
    """
    if listings_collection is None:
        return False

    # Required fields for the unique key
    source = listing_data.get("source")
    external_id = listing_data.get("external_id")

    if not source or not external_id:
        print("Error: Listing data missing 'source' or 'external_id'.")
        return False

    # Query to find existing document
    query = {"source": source, "external_id": external_id}

    # Update document with new data and metadata
    update_data = {
        "$set": {
            **listing_data,
            "last_seen": datetime.utcnow(),
            "status": "active",
        },
        "$setOnInsert": {
            "first_seen": datetime.utcnow(),
        }
    }

    try:
        result = listings_collection.update_one(
            query,
            update_data,
            upsert=True  # Insert if no document matches the query
        )
        return result.acknowledged
    except Exception as e:
        print(f"Error during upsert: {e}")
        return False

def bulk_upsert_listings(listings: List[Dict[str, Any]]) -> int:
    """
    Performs a bulk upsert operation for a list of listings.
    """
    if listings_collection is None:
        return 0

    operations = []
    for listing_data in listings:
        source = listing_data.get("source")
        external_id = listing_data.get("external_id")

        if not source or not external_id:
            continue

        query = {"source": source, "external_id": external_id}
        update_data = {
            "$set": {
                **listing_data,
                "last_seen": datetime.utcnow(),
                "status": "active",
            },
            "$setOnInsert": {
                "first_seen": datetime.utcnow(),
            }
        }

        operations.append(
            pymongo.UpdateOne(query, update_data, upsert=True)
        )

    if not operations:
        return 0

    try:
        import pymongo
        result = listings_collection.bulk_write(operations, ordered=False)
        return result.upserted_count + result.modified_count
    except Exception as e:
        print(f"Error during bulk upsert: {e}")
        return 0

# Initialize indexes when the module is loaded
if listings_collection:
    setup_mongo_indexes()

# Example GeoJSON Query function (for Map View)
def find_listings_near(longitude: float, latitude: float, max_distance_km: float, min_price: int = None, max_price: int = None) -> List[Dict[str, Any]]:
    """
    Finds listings near a given point using GeoJSON and 2dsphere index.
    max_distance_km is converted to meters for MongoDB.
    """
    if listings_collection is None:
        return []

    max_distance_meters = max_distance_km * 1000

    # GeoJSON query
    geo_query = {
        "location.coordinates": {
            "$nearSphere": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": [longitude, latitude]
                },
                "$maxDistance": max_distance_meters
            }
        }
    }

    # Price filtering
    price_query = {}
    if min_price is not None:
        price_query["price"] = {"$gte": min_price}
    if max_price is not None:
        if "price" in price_query:
            price_query["price"]["$lte"] = max_price
        else:
            price_query["price"] = {"$lte": max_price}

    # Combine queries
    final_query = {**geo_query, **price_query}

    try:
        # Fetch and convert to list
        results = list(listings_collection.find(final_query).limit(100))
        return results
    except Exception as e:
        print(f"Error during geospatial query: {e}")
        return []

# Example function to mark all old listings as inactive (optional, as TTL handles removal)
def mark_old_listings_inactive(days_old: int = 7):
    """
    Marks listings that haven't been seen in 'days_old' as inactive.
    This is a fallback/status update, as TTL handles removal.
    """
    if listings_collection is None:
        return 0

    cutoff_date = datetime.utcnow() - timedelta(days=days_old)
    result = listings_collection.update_many(
        {"last_seen": {"$lt": cutoff_date}, "status": "active"},
        {"$set": {"status": "inactive"}}
    )
    return result.modified_count

# Helper function to get all active listings (for the main search view)
def get_all_active_listings(limit: int = 100) -> List[Dict[str, Any]]:
    """
    Retrieves all active listings, sorted by last seen date.
    """
    if listings_collection is None:
        return []

    try:
        results = list(
            listings_collection.find({"status": "active"})
            .sort("last_seen", -1)
            .limit(limit)
        )
        return results
    except Exception as e:
        print(f"Error retrieving active listings: {e}")
        return []
