## 2025-11-20 - Standardizing Accessibility Patterns

**Learning:** This repository uses Font Awesome icons extensively for visual cues (homes, beds, baths, prices). These are purely decorative but were being announced by screen readers. Additionally, generic buttons like "View Listing" are repetitive and unhelpful without context in the accessibility tree.

**Action:** Standardized the use of `aria-hidden="true"` on all `<i>` tags for decorative icons. Implemented dynamic `aria-label` on listing buttons to include the listing title, and used `aria-describedby` to link form inputs with their helper text.
