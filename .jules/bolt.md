## 2026-03-15 - Surgical Scraper Optimizations
**Learning:** For large HTML documents like Kijiji search results, regex-based extraction of JSON-LD content is order of magnitude faster than full DOM parsing. Also, centralized parser selection (lxml vs html.parser) and length-based short-circuits for SequenceMatcher are effective low-risk wins.
**Action:** Use regex to extract structured data from large pages; provide a base class helper for parser selection to avoid code repetition.
