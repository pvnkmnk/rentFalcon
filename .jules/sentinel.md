## 2026-04-01 - CSRF Protection and API Exemption
**Vulnerability:** The application lacked CSRF protection on its main search form and used a hardcoded SECRET_KEY.
**Learning:** When enabling global CSRF protection in Flask, programmatic API endpoints (like /api/search) must be explicitly exempted using @csrf.exempt if they are intended for non-browser/stateless access.
**Prevention:** Always initialize CSRFProtect and use environment variables for sensitive configurations. Verify API accessibility in security tests after enabling protection.
