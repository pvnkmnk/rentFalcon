## 2026-03-28 - CSRF Protection Implementation and Secret Key Management
**Vulnerability:** The application's search form lacked Cross-Site Request Forgery (CSRF) protection, and the `SECRET_KEY` was hardcoded in the source code.
**Learning:** CSRF protection in Flask is easily implemented with `flask-wtf`, but it must be explicitly initialized. Hardcoded secrets are a critical vulnerability that undermines security measures like CSRF.
**Prevention:** Always use `CSRFProtect` for Flask applications with forms, and ensure `SECRET_KEY` is loaded from environment variables in production. Exempt programmatic API endpoints from CSRF using `@csrf.exempt`.
