## 2026-03-19 - O(n²) Deduplication Short-Circuit
**Learning:** `difflib.SequenceMatcher` is computationally expensive for calculating text similarity in O(n²) deduplication logic. A simple length-based check `(2.0 * min(len1, len2) / (len1 + len2))` can skip the comparison entirely for strings that can't possibly meet the similarity threshold.
**Action:** Implement length-based short-circuit in `_text_similarity` method of `ScraperManager` to reduce overhead on non-matching pairs.

## 2026-03-19 - Careful Threshold Application in Short-Circuits
**Learning:** When using short-circuit optimizations with thresholds, ensure the threshold passed to the helper function is the *minimum* required for all subsequent logic that uses the result. Passing a high threshold early can cause functional regressions by returning `0.0` for strings that would have matched a lower threshold fallback later.
**Action:** Use the minimum required threshold (`0.7` in the case of `ScraperManager`) for initial similarity checks that serve as inputs to multiple conditional branches.
