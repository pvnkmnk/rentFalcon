## 2025-05-22 - Search Interaction and Listing Accessibility

**Learning:** When a search takes several seconds, providing immediate visual feedback on the button itself (disabling and showing a "Searching..." state) reduces user uncertainty and prevents multiple form submissions. Additionally, repetitive buttons like "View Listing" need dynamic context in their `aria-label` to be distinguishable by screen reader users.

**Action:** Always implement a loading state for the primary action button on long-running tasks. Use template variables to inject context into `aria-label` for list items to ensure accessibility.
