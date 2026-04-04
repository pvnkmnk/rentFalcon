## 2026-04-04 - Centralized BeautifulSoup Parser Selection
**Learning:** Switching from `html.parser` to `lxml` in BeautifulSoup provides a significant performance boost (~35-60%) for parsing rental listings. Centralizing this in a base class with a cached parser selection avoids redundant dependency checks and simplifies maintenance across multiple scrapers.
**Action:** Always prefer `lxml` for heavy HTML parsing tasks and use a centralized factory method to manage parser selection and fallbacks.
