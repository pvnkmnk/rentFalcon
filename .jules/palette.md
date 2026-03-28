## 2025-05-15 - Improving Search Loading State and Accessibility

**Learning:** Enhancing the search button's internal state (disabling, spinner, and text update) alongside a full-page loading overlay provides immediate visual feedback at the point of interaction, which is especially important for multi-source scraping operations that can take several seconds.

**Action:** Always pair a global loading overlay with local button state changes to ensure users receive clear, immediate feedback that their action was registered, even before the overlay appears or if it fails to show.

**Learning:** Repetitive decorative icons (like Font Awesome <i> tags) should be consistently marked with `aria-hidden="true"` to prevent screen readers from announcing them, which can significantly clutter the user's experience on listing-heavy pages.

**Action:** Audit all icon usage in templates and apply `aria-hidden="true"` to any element that doesn't convey unique information not already present in the adjacent text.
