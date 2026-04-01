## 2026-03-30 - Missing CSRF Protection in Main Search Form
**Vulnerability:** The main rental search form in `templates/index.html` was missing CSRF protection, allowing potential Cross-Site Request Forgery attacks.
**Learning:** Although `Flask-WTF` was listed in `requirements.txt`, it was not initialized in the application. Dependencies alone do not provide security; they must be correctly integrated and configured.
**Prevention:** Explicitly initialize `CSRFProtect(app)` in the main application entry point and include `{{ csrf_token() }}` in all POST forms. Add automated security tests that specifically attempt POST requests without tokens to ensure protection remains active.
