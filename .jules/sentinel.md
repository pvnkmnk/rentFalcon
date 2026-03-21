## 2025-05-15 - Global CSRF Protection and Dynamic Configuration
**Vulnerability:** Hardcoded `SECRET_KEY` and missing CSRF protection on the main search form.
**Learning:** Defaulting to global `CSRFProtect` in Flask-WTF is safer than per-view protection, but requires explicit exemptions for programmatic APIs (`@csrf.exempt`) to avoid breaking external integrations.
**Prevention:** Always use `app.config.from_object` with environment-aware configuration and initialize `CSRFProtect` early in the app lifecycle.
