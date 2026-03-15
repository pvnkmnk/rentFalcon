## 2026-03-15 - Enhancing Context for Repetitive Call-to-Actions
**Learning:** Generic button text like "View Listing" can be problematic for screen reader users when multiple instances appear on a page, as they lack unique context in the link list.
**Action:** Always provide descriptive ARIA labels for repetitive action buttons, incorporating dynamic content (e.g., listing titles) to ensure each action is clearly distinguishable.

## 2026-03-15 - Capturing Ephemeral Loading States
**Learning:** Standard Playwright screenshots often miss fast-transitioning loading states (like button spinners) because the navigation happens too quickly or the script doesn't time the capture perfectly.
**Action:** Use `e.preventDefault()` in a temporary `page.evaluate` script during verification to "freeze" the UI in its loading state for reliable visual inspection.
