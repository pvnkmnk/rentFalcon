## 2025-03-24 - Search Button Feedback and bfcache Resilience
**Learning:** Using `pageshow` instead of `load` for resetting UI states (like loading spinners) is critical for modern browsers that use the Back-Forward Cache (bfcache). This ensures that if a user submits a form and then clicks "Back", the button isn't still in its "Searching..." disabled state.
**Action:** Prefer `pageshow` event listeners for UI state resets to ensure resilience during browser navigation.

## 2025-03-24 - Dynamic Context for Generic Buttons
**Learning:** Screen reader users benefit significantly from dynamic `aria-label` attributes on repetitive buttons like "View Listing". Providing the listing title in the label (e.g., "View listing for [Property Title]") gives immediate context without needing to read the surrounding card.
**Action:** Always include entity-specific context in ARIA labels for repetitive action buttons in lists or cards.
