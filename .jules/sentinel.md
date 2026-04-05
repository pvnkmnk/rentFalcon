# 🛡️ Sentinel Journal

## 2026-04-05 - Global CSRF Protection and Config Centralization
**Vulnerability:** The application was not using CSRF protection for its main search form, allowing potential Cross-Site Request Forgery attacks. Additionally, the Flask configuration was partially hardcoded in `app.py`, bypassing the robust settings in `config.py`.

**Learning:** Initializing `CSRFProtect(app)` in Flask-WTF provides global protection for all POST, PUT, PATCH, and DELETE requests by default. For programmatic APIs that don't rely on session cookies (like `/api/search`), explicit exemption using `@csrf.exempt` is necessary.

**Prevention:** Always use a centralized configuration manager and ensure CSRF protection is enabled from the start of a project. When using Flask-WTF, verify that every template with a POST form includes the `{{ csrf_token() }}` helper.
