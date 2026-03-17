## 2026-03-17 - CSRF Protection and Security Headers
**Vulnerability:** The application lacked Cross-Site Request Forgery (CSRF) protection and important security headers, leaving it vulnerable to session hijacking, clickjacking, and content injection.
**Learning:** Enabling global CSRF protection in Flask with 'Flask-WTF' is straightforward but requires consistent template updates and explicit exemptions for programmatic API endpoints to avoid breaking 3rd-party integrations.
**Prevention:** Always use 'Flask-WTF' for CSRF protection and implement an 'after_request' hook to enforce a robust Content Security Policy and other standard security headers.
