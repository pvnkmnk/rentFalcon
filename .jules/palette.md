## 2026-04-06 - Enhancing search feedback and accessibility

**Learning:** Providing both local (button state) and global (overlay) feedback during long-running async operations significantly improves the perceived responsiveness of the application. Using the `pageshow` event is more reliable than `load` for resetting UI states during browser navigation (back/forward buttons).

**Action:** Always implement `pageshow` listeners when disabling buttons or showing overlays on form submission to prevent broken UI states on navigation.
