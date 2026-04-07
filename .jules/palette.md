## 2026-04-07 - Interactive Search Feedback & A11y Polish

**Learning:** Combining local feedback (disabling button, showing spinner, updating text) with global feedback (full-page loading overlay) provides a more responsive feel for long-running operations. Additionally, the browser's Back-Forward Cache (BFCache) can leave interactive elements in a disabled state when a user navigates back; using the `pageshow` event is a reliable way to reset the UI state.

**Action:** Always implement a reset function triggered by `pageshow` when disabling buttons or showing overlays upon form submission. Ensure decorative icons are hidden from screen readers with `aria-hidden="true"` and interactive elements have descriptive context-aware labels.
