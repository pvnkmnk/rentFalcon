## 2026-03-18 - Initial Performance Assessment
**Learning:** Initial profiling shows that scrapers use `html.parser` instead of `lxml`, and deduplication uses `SequenceMatcher` without optimizations. Selenium is a major bottleneck but is necessary for some sites.
**Action:** Focus on optimizing the most frequently called parts of the code: BeautifulSoup parsing and deduplication logic.
