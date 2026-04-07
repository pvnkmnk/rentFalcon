import time
from bs4 import BeautifulSoup
import os


def benchmark_parser(html_content, parser_name):
    start = time.time()
    for _ in range(100):
        soup = BeautifulSoup(html_content, parser_name)
        _ = soup.find_all("div")
    end = time.time()
    return end - start


def main():
    # Create a dummy large HTML
    dummy_html = (
        "<html><body>"
        + "<div><p>Some text</p><span>More text</span></div>" * 1000
        + "</body></html>"
    )

    print(f"Benchmarking with {len(dummy_html)} bytes of HTML...")

    time_html_parser = benchmark_parser(dummy_html, "html.parser")
    print(f"html.parser: {time_html_parser:.4f}s")

    try:
        time_lxml = benchmark_parser(dummy_html, "lxml")
        print(f"lxml: {time_lxml:.4f}s")
        improvement = (time_html_parser - time_lxml) / time_html_parser * 100
        print(f"Improvement: {improvement:.2f}%")
    except Exception as e:
        print(f"lxml not available or failed: {e}")


if __name__ == "__main__":
    main()
