## 2026-03-25 - Contextual Accessibility for Repetitive Actions
**Learning:** Repetitive buttons with generic text (e.g., "View Listing") in search results present a challenge for screen reader users who navigate by interactive elements. Providing dynamic context in the ARIA label improves navigation significantly.
**Action:** Always include the item's title or unique identifier in the `aria-label` for repetitive list-based action buttons (e.g., `aria-label="View listing for {{ listing.title }}"`).

## 2026-03-25 - Synchronized Loading States
**Learning:** For long-running async operations (like multi-source scraping), providing feedback both at the page level (overlay) and the trigger level (button) ensures users feel the interaction was successful even if the overlay has a slight transition delay.
**Action:** Implement immediate button-level state changes (disable, spinner, text update) alongside global loading indicators.
