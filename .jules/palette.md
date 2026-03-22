## 2025-05-15 - [UI Logic Centralization & Input Clarity]
**Learning:** Moving loading state logic from inline scripts to a dedicated JavaScript file (`static/js/script.js`) significantly improves maintainability and allows for more robust handling of ephemeral UI states, such as re-enabling buttons on `pageshow`. Additionally, using Bootstrap input groups with both prefix ($) and suffix (/mo) for currency fields provides immediate, unambiguous context that reduces user cognitive load compared to standard labels alone.
**Action:** Always prioritize moving inline UI logic to external scripts and use descriptive input groups for numerical values requiring units.

## 2025-05-15 - [Accessibility Baseline for Iconography]
**Learning:** Decorative icons (e.g., Font Awesome) must be consistently marked with `aria-hidden="true"` to prevent screen reader noise. Icon-only or icon-heavy buttons require explicit `aria-label` attributes that include dynamic context (like listing titles) to provide a meaningful experience for assistive technology users.
**Action:** Audit all templates for Font Awesome usage and ensure `aria-hidden` or `aria-label` are applied based on the icon's role.
