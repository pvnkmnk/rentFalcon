## 2025-05-15 - [CSRF Protection Implementation]
**Vulnerability:** The application accepted POST requests to the main search page without any CSRF validation, making it vulnerable to Cross-Site Request Forgery.
**Learning:** Enabling `CSRFProtect` globally in a Flask app requires all POST forms in templates to include a `csrf_token`. Programmatic APIs (like `/api/search`) should be explicitly exempted using `@csrf.exempt` if they are intended for external use without session-based auth.
**Prevention:** Always use `Flask-WTF` for CSRF protection in Flask applications and ensure all forms include the CSRF token.
