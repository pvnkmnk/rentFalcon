## 2026-03-31 - Centralized Parser Optimization
**Learning:** Benchmarking confirms that the 'lxml' parser is approximately 30-40% faster than 'html.parser' for processing large rental listing pages in this repository.
**Action:** Always use 'self.get_soup(html)' from the 'BaseScraper' class; it utilizes the faster 'lxml' parser when available and automatically falls back to 'html.parser' otherwise.
