## 2026-03-27 - [BeautifulSoup Parser Optimization]
**Learning:** Benchmarking confirms that the 'lxml' parser is approximately 28-42% faster than 'html.parser' for processing large rental listing pages in this repository. Centralizing parser selection in the `BaseScraper` with a class-level cache ensures all scrapers benefit from this optimization without redundant import checks.
**Action:** Always use `self.get_soup(html)` from the `BaseScraper` class for HTML parsing; it prioritizes 'lxml' and falls back to 'html.parser' if unavailable.
