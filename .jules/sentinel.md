## 2026-03-20 - CSRF Protection and Config Loading
**Vulnerability:** Missing CSRF protection on search form and hardcoded SECRET_KEY in app.py.
**Learning:** Initializing CSRFProtect globally in app.py requires all POST forms in templates to include a `csrf_token` hidden field. Exempting programmatic API endpoints with `@csrf.exempt` is necessary to maintain compatibility with external clients. Loading configuration from a dedicated `config.py` module improves security by allowing secrets to be managed via environment variables.
**Prevention:** Always use `Flask-WTF` for CSRF protection and load configuration using a class-based system from `config.py`.
