## 2026-03-16 - Text Similarity Short-Circuit
**Learning:** `difflib.SequenceMatcher.ratio()` is computationally expensive ($O(N \times M)$). However, it has a mathematical upper bound based on string lengths: $(2.0 \times \min(len1, len2)) / (len1 + len2)$.
**Action:** Use this $O(1)$ length-based check to short-circuit similarity calculations when the maximum possible ratio is already below the target threshold. This provides a massive speedup (up to 90x in benchmarks) for comparing strings of significantly different lengths.

## 2026-03-16 - Regex vs BeautifulSoup for JSON-LD
**Learning:** While `re.search` is significantly faster (~180x) than full DOM parsing with `BeautifulSoup` for extracting JSON-LD, it is riskier and can be brittle (e.g., matching commented-out scripts or incorrect script types).
**Action:** Prefer robust parsing over micro-optimizations in core scraping logic unless the performance bottleneck is severe and cannot be solved otherwise. Focus optimizations on algorithmic improvements (like short-circuits) rather than replacing standard parsers with regex.
