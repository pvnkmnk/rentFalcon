## 2026-03-29 - Progressive Search Feedback and Form Accessibility

**Learning:** Implementing both a global loading overlay and local button feedback provides better immediate response for users. In multi-source search apps where tasks can take several seconds, visual confirmation that the button "clicked" and is "working" reduces repeat clicks and user frustration. Standardizing ARIA labels and hiding decorative icons ensures a consistent experience for screen reader users across the entire results list.

**Action:** Use a dual-layer feedback approach (button state + full-page overlay) for long-running processes. Always ensure icons in interactive elements are either described by the text or hidden from ARIA if decorative.
