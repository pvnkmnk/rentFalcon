## 2025-05-15 - HTML Parsing Optimization with lxml
**Learning:** Benchmarking confirms that the 'lxml' parser is approximately 30-50% faster than 'html.parser' for processing large rental listing pages in this repository.
**Action:** Always use `self.get_soup(html)` from `BaseScraper` to leverage the centralized 'lxml' optimization and ensure consistent, high-performance parsing across all scrapers.
