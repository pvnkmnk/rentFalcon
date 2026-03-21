## 2026-03-21 - Centralize and optimize HTML parsing with lxml
**Learning:** Benchmarking confirms that the 'lxml' parser is approximately 33-42% faster than the default 'html.parser' for processing large rental listing pages in this repository. Centralizing BeautifulSoup parsing in a base class method (`get_soup`) ensures consistent use of the fastest available parser across all scrapers while providing a robust fallback.
**Action:** Always use `self.get_soup(html)` in scrapers instead of calling `BeautifulSoup(html, "html.parser")` directly.
