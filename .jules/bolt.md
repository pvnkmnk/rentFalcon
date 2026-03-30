## 2025-05-15 - Optimizing `SequenceMatcher` with Length-Based Pre-filter
**Learning:** `difflib.SequenceMatcher.ratio()` is $O(N \times M)$ and becomes a significant bottleneck when deduplicating large numbers of listings (e.g., >1000). A mathematical upper bound for the ratio can be calculated as `2.0 * min(len1, len2) / (len1 + len2)`. If this upper bound is below the required threshold, the expensive computation can be skipped entirely.
**Action:** Always implement length-based pre-filters when using `SequenceMatcher` in a loop over large datasets. Ensure that the optimization doesn't accidentally return the upper bound as a substitute for the actual score if that would cause logic errors (though for "greater than threshold" checks, returning the upper bound is safe as long as the bound itself is below the threshold).

## 2025-05-15 - Handling Missing Titles in Deduplication
**Learning:** Initializing `title_similarity = 0.0` is crucial in `_listings_similar` to prevent `UnboundLocalError` when one or both listings lack titles, as the title similarity check is bypassed in those cases but referenced later in the location similarity check.
**Action:** Ensure all variables used in multi-stage similarity logic are properly initialized to safe defaults.
