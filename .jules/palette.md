## 2025-11-04 - Enhanced Multi-Layer Search Feedback

**Learning:** Providing feedback at both the component level (button text/spinner) and the layout level (full-page overlay) creates a more robust sense of "work in progress" for long-running operations like multi-source scraping. Using the `pageshow` event instead of `load` ensures that UI states are correctly reset when navigating back through the browser history, preventing "stuck" buttons.

**Action:** Always use `pageshow` for resetting ephemeral UI states to support bfcache-capable browsers. Combine local and global feedback for any task exceeding 2 seconds.
