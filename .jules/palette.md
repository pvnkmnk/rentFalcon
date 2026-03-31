## 2026-03-31 - Dual-Layer Search Feedback and Micro-UX Accessibility
**Learning:** Combining local feedback (disabling button, updating text/spinner) with global feedback (full-page overlay) provides the most responsive feel for long-running search operations. Additionally, standardizing ARIA attributes for decorative icons and contextual links significantly improves the screen reader experience in listing-heavy interfaces.
**Action:** Always implement immediate button state changes alongside loading overlays to ensure zero-latency feedback for primary user actions.
