## 2026-04-08 - Centralized UI Logic and Accessibility
**Learning:** Moving inline UI logic to a centralized script file improves maintainability and allows for more robust state management (e.g., handling `pageshow` for back-button resets). Mandatory accessibility attributes like `aria-hidden` for decorative icons and `aria-label` for context-specific buttons are essential for screen reader users and often missing in Bootstrap templates.
**Action:** Always link external scripts for UI logic and audit for missing ARIA attributes in all templates.

## 2026-04-08 - Verifying Refactored Selectors
**Learning:** When refactoring or moving JS logic to external files, it is crucial to verify that all DOM selectors used in the script actually exist in the HTML. A mismatch between script selectors (e.g., `.results-card`) and template classes can silently break functionality like sorting or filtering.
**Action:** Use Playwright to specifically test interactive features (sorting, filtering) after refactoring JS selectors.
