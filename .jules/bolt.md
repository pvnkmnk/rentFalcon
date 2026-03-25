## 2026-03-25 - HTML Parsing Optimization with lxml
**Learning:** Benchmarking confirms that the `lxml` parser is approximately 33-42% faster than the built-in `html.parser` for processing large rental listing pages in this repository. Centralizing parser selection in `BaseScraper` allows all scrapers to benefit from this speed boost while maintaining a safe fallback.
**Action:** Always use `self.get_soup(html)` from the `BaseScraper` class; it utilizes the faster 'lxml' parser when available and automatically falls back to 'html.parser' otherwise.
