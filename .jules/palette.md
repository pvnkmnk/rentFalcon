
## 2025-05-14 - Redundant Icon Announcements and BFCache State Reset
**Learning:** Purely decorative icons (like Font Awesome) should always have `aria-hidden="true"` to avoid redundant or confusing screen reader announcements. Additionally, when disabling buttons on form submission to prevent multiple clicks, it is essential to handle the `pageshow` event to reset the button state for users who navigate back to the page via browser history.
**Action:** Always include `aria-hidden="true"` for decorative icons and implement a `pageshow` listener to ensure UI responsiveness during back/forward navigation.
