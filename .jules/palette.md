## 2025-03-30 - Multi-Layered Search Feedback
**Learning:** Providing immediate local feedback (disabling button, showing spinner, updating text) in addition to a global loading overlay significantly improves perceived responsiveness and prevents duplicate form submissions.
**Action:** Always implement local button state changes alongside global overlays for long-running operations.

## 2025-03-30 - Contextual Link Labels
**Learning:** "View Listing" links are vague for screen reader users when multiple listings are present. Adding the property title to the ARIA label provides necessary context.
**Action:** Use `aria-label="View listing for [Title]"` instead of generic link text.
