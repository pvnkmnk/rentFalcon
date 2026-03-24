## 2026-03-24 - Optimizing String Similarity and HTML Parsing

**Learning:** `difflib.SequenceMatcher.ratio()` is a major bottleneck in O(N^2) deduplication tasks. Using `real_quick_ratio()` and `quick_ratio()` as early short-circuits can save significant CPU cycles for pairs that are clearly dissimilar. Additionally, `lxml` is ~35% faster than `html.parser` for BeautifulSoup.

**Action:** Always provide a `get_soup` helper that defaults to `lxml`. In fuzzy matching, use upper-bound checks to skip expensive exact ratio calculations when the result is guaranteed to be below the target threshold.
