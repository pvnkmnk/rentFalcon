import time
import logging
from scrapers.scraper_manager import ScraperManager
import random
import string

# Disable logging for benchmark
logging.basicConfig(level=logging.ERROR)


def generate_random_string(length=50):
    return "".join(random.choices(string.ascii_lowercase + " ", k=length))


def benchmark_actual_manager(num_listings):
    manager = ScraperManager()
    listings = []
    for _ in range(num_listings):
        listings.append(
            {
                "title": generate_random_string(),
                "location": generate_random_string(),
                "price": random.randint(1000, 3000),
                "url": None,  # Force fuzzy matching
            }
        )

    start = time.time()
    # manager._deduplicate_listings is what we want to benchmark
    unique_listings = manager._deduplicate_listings(listings)
    end = time.time()
    return end - start


def main():
    print("Benchmarking ScraperManager._deduplicate_listings...")
    for n in [50, 100, 200]:
        t = benchmark_actual_manager(n)
        print(f"Deduplicating {n} listings took {t:.4f}s")


if __name__ == "__main__":
    main()
