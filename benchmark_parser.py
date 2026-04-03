
import time
from bs4 import BeautifulSoup
import os

# Generate a moderately large HTML for testing
html_content = "<html><body>" + "".join([f"<div class='listing-card' id='{i}'><h2>Listing {i}</h2><p class='price'>$1{i}00</p><p class='location'>Location {i}</p><a href='/listing/{i}'>Link</a></div>" for i in range(1000)]) + "</body></html>"

def benchmark(parser, content, iterations=10):
    start_time = time.time()
    for _ in range(iterations):
        soup = BeautifulSoup(content, parser)
        cards = soup.find_all("div", class_="listing-card")
    end_time = time.time()
    return (end_time - start_time) / iterations

print(f"Benchmarking with {len(html_content)} bytes of HTML...")
html_parser_time = benchmark("html.parser", html_content)
print(f"html.parser average time: {html_parser_time:.4f}s")

try:
    lxml_parser_time = benchmark("lxml", html_content)
    print(f"lxml average time: {lxml_parser_time:.4f}s")
    improvement = (html_parser_time - lxml_parser_time) / html_parser_time * 100
    print(f"Improvement: {improvement:.2f}%")
except Exception as e:
    print(f"lxml benchmark failed: {e}")
