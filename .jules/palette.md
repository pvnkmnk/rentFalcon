## 2025-05-15 - Multi-Source Search Feedback & Accessibility Enhancements

**Learning:** Enhancing user feedback during multi-source searches significantly improves perceived responsiveness and reduces user anxiety. Accessible design, such as hiding decorative icons from screen readers and providing descriptive ARIA labels, is essential for an inclusive and professional interface.

**Action:** Standardize the use of `aria-hidden="true"` for decorative icons and `aria-label` for links/buttons in all future UI components. Always implement loading states (button disabling, text change, and spinners) for asynchronous or long-running operations. Ensure UI state resets properly during browser navigation (e.g., using the `pageshow` event).
