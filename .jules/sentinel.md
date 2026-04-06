## 2026-04-06 - Implement CSRF Protection and Centralized Configuration
**Vulnerability:** Hardcoded `SECRET_KEY` in `app.py` and missing CSRF protection on the main search form.
**Learning:** Hardcoded secrets are a critical vulnerability that should be moved to a centralized configuration. CSRF protection is essential for state-changing POST requests, but standard programmatic APIs might need exemptions if they don't rely on session cookies.
**Prevention:** Use `Flask-WTF` for global CSRF protection and always load configuration from a separate module that pulls from environment variables. Verify protection with automated tests using the Flask test client.
