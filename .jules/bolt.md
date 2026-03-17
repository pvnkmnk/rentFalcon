# ⚡ Bolt's Journal - Performance Optimizations

This journal records critical performance learnings and insights for the rentFalcon project.

## 2026-03-17 - BeautifulSoup Parser Optimization
**Learning:** The default `html.parser` is noticeably slower than `lxml`, especially on large listing pages like Kijiji. A benchmark showed ~37% improvement in parsing time when using `lxml`.
**Action:** Implemented a centralized `get_soup` method in `BaseScraper` that defaults to `lxml` with a safe fallback to `html.parser`. All scrapers were updated to use this method.

## 2026-03-17 - Rejected: Similarity Short-circuit
**Learning:** While a length-based short-circuit for `SequenceMatcher` can drastically improve speed for disparate strings, returning the `max_ratio` (upper bound) instead of the actual ratio is a functional regression if other parts of the system depend on accurate similarity scores.
**Action:** Reverted the optimization to maintain functional correctness. In the future, a more surgical approach that only skips comparison when *definitely* below the threshold (but still returns the actual ratio if needed) or a more robust caching mechanism should be considered.
