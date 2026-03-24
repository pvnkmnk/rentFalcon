## 2026-03-24 - [Micro-UX: Search Loading States & Accessibility]
**Learning:** Micro-UX logic (JS/CSS) should be implemented inline within template files to ensure patches remain self-contained and portable, adhering to the 50-line PR limit while avoiding dependency on missing static assets.
**Action:** Favor inline scripts/styles for small UI enhancements instead of creating/linking new external files.

**Learning:** ARIA labels on icon-only buttons or repetitive links (like "View Listing") should include dynamic context (e.g., listing title) to provide meaningful information to screen reader users.
**Action:** Use template variables to enrich aria-labels: `aria-label="View listing for {{ listing.title }}"`.
