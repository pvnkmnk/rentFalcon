## 2025-05-15 - Improving Accessibility for Repetitive Listing Links and Providing Immediate Search Feedback

**Learning:** In listing aggregators, repetitive buttons like "View Listing" can be confusing for screen reader users if they lack context. Adding dynamic ARIA labels that include the listing title significantly improves navigation. Additionally, disabling the search button and providing a loading state prevents double submissions and reduces user anxiety during long-running background tasks.

**Action:** Always add descriptive `aria-label` to repetitive actions within loops. Implement immediate visual and functional feedback (disabling + spinner) on buttons that trigger asynchronous or slow processes.
