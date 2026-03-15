## 2026-03-15 - CSRF Protection Implementation
**Vulnerability:** Missing CSRF (Cross-Site Request Forgery) protection on search form POST requests.
**Learning:** Even simple search forms using POST can be vulnerable to CSRF, allowing attackers to force users to perform searches. While search is often idempotent, it can be used for usage tracking or as a vector for other attacks if results are reflected without proper sanitization. In this app, CSRF protection was missing despite `Flask-WTF` being available in dependencies.
**Prevention:** Always initialize `CSRFProtect(app)` and include `{{ csrf_token() }}` in all HTML forms. For programmatic APIs, explicitly document whether CSRF is required or exempt them if they use other authentication methods.
