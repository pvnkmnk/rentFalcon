
import time
from bs4 import BeautifulSoup

def benchmark_parsers(html_content, iterations=100):
    print(f"Benchmarking with {iterations} iterations...")

    # Benchmark html.parser
    start_time = time.time()
    for _ in range(iterations):
        soup = BeautifulSoup(html_content, "html.parser")
        _ = soup.find_all("a")
    html_parser_time = time.time() - start_time
    print(f"html.parser: {html_parser_time:.4f} seconds")

    # Benchmark lxml
    try:
        start_time = time.time()
        for _ in range(iterations):
            soup = BeautifulSoup(html_content, "lxml")
            _ = soup.find_all("a")
        lxml_time = time.time() - start_time
        print(f"lxml: {lxml_time:.4f} seconds")
        print(f"Speedup: {html_parser_time / lxml_time:.2f}x")
    except Exception as e:
        print(f"lxml failed: {e}")

if __name__ == "__main__":
    # Create a reasonably large HTML content
    html_content = "<html><body>" + "".join([f"<div><a href='#'>{i}</a><p>Some text {i}</p></div>" for i in range(1000)]) + "</body></html>"
    benchmark_parsers(html_content)
