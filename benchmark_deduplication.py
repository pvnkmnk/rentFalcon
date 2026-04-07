import time
from difflib import SequenceMatcher
import random
import string


def text_similarity(text1, text2):
    return SequenceMatcher(None, text1, text2).ratio()


def generate_random_string(length=50):
    return "".join(random.choices(string.ascii_lowercase + " ", k=length))


def benchmark_deduplication(num_listings):
    listings = []
    for _ in range(num_listings):
        listings.append(
            {
                "title": generate_random_string(),
                "location": generate_random_string(),
                "price": random.randint(1000, 3000),
                "url": f"https://example.com/{generate_random_string(10)}",
            }
        )

    start = time.time()
    unique_listings = []
    for listing in listings:
        is_dup = False
        for existing in unique_listings:
            # Simplified version of ScraperManager._listings_similar
            if listing["url"] == existing["url"]:
                is_dup = True
                break

            # Simulate expensive text similarity
            t_sim = text_similarity(listing["title"], existing["title"])
            if t_sim > 0.85:
                l_sim = text_similarity(listing["location"], existing["location"])
                if l_sim > 0.85:
                    is_dup = True
                    break

        if not is_dup:
            unique_listings.append(listing)

    end = time.time()
    return end - start


def main():
    for n in [50, 100, 200]:
        t = benchmark_deduplication(n)
        print(f"Deduplicating {n} listings took {t:.4f}s")


if __name__ == "__main__":
    main()
