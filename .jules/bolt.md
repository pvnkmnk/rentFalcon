## 2026-03-20 - SequenceMatcher Optimization for Deduplication
**Learning:** Using `SequenceMatcher.ratio()` is (N^2)$ and can be a major bottleneck when deduplicating large sets of strings. `real_quick_ratio()` and `quick_ratio()` provide fast upper bounds.
**Action:** Always use `real_quick_ratio()` and `quick_ratio()` for early exits when comparing strings against a threshold. Also, ensure variables used in combined conditional checks (like title and location similarity) are initialized to handle cases where one piece of data might be missing.
