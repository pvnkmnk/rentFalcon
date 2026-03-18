## 2025-05-14 - Accessible Icon and Button Patterns
**Learning:** Found a systemic pattern of decorative icons (Font Awesome) being announced by screen readers and repetitive "View Listing" buttons lacking context, which is common in listing-heavy aggregators.
**Action:** Always apply `aria-hidden="true"` to <i> tags used for decoration and use dynamic `aria-label` attributes for buttons in loops to include unique identifiers (e.g., listing titles).

## 2025-05-14 - Verifying Ephemeral UI States
**Learning:** Testing loading states on buttons during form submissions is difficult due to rapid page reloads.
**Action:** Use `page.evaluate` to add a capturing-phase event listener that calls `e.preventDefault()` on the form to freeze the UI in its loading state for screenshot capture.
