# Palette's Journal - Critical UX/Accessibility Learnings

## 2025-05-14 - Initializing Journal
**Learning:** Initializing the journal for the rentFalcon project.
**Action:** Always document critical UX and accessibility insights here.

## 2026-03-17 - Accessibility Patterns for Aggregators
**Learning:** In a listing aggregator, repeated actions like "View Listing" lack context for screen readers. Decorative icons in headers and badges also clutter the accessibility tree.
**Action:** Use `aria-label` with dynamic listing titles for repetitive buttons and apply `aria-hidden="true"` to all decorative Font Awesome icons.

## 2026-03-17 - Currency Input Pattern
**Learning:** Using Bootstrap `input-group` with `$` and `/mo` addons significantly improves the intuition of price range filters compared to plain placeholders.
**Action:** Prefer `input-group` for currency and unit-based numeric inputs.
