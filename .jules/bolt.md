## 2025-05-14 - Optimized fuzzy matching in O(n²) deduplication
**Learning:** Performing string normalization (lower/strip) inside a nested loop for fuzzy matching is a significant bottleneck as it repeats the same operations O(n²) times. Short-circuiting exact matches before invoking `difflib.SequenceMatcher` provides a major speed boost because `SequenceMatcher` is computationally expensive.
**Action:** Always pre-calculate normalized values before entering $O(n^2)$ loops and use short-circuits for identical inputs in similarity functions.
