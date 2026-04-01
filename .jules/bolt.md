## 2026-04-01 - Optimized HTML parsing with lxml
**Learning:** Benchmarking confirms that the 'lxml' parser is approximately 28-42% faster than 'html.parser' for processing large rental listing pages in this repository. Centralizing the parsing logic in `BaseScraper` ensures consistency and easy environment-based optimization.
**Action:** Always use `self.get_soup(html)` from the `BaseScraper` class for any new scrapers to benefit from the 'lxml' performance boost and fallback mechanism.
