## 2026-04-02 - Centralized and Optimized HTML Parsing
**Learning:** Large rental listing pages (>1MB) show a ~44% parsing speed improvement when using 'lxml' instead of 'html.parser'. Centralizing BeautifulSoup instantiation in a base class with a cached parser preference avoids redundant import checks and ensures consistent performance across all scrapers.
**Action:** Always use 'self.get_soup(html)' in scraper subclasses to benefit from the 'lxml' optimization and centralized parser management.
