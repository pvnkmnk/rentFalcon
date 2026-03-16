## 2026-03-16 - Configuration Loading and CSRF Protection
**Vulnerability:** Hardcoded SECRET_KEY and missing CSRF protection on the main search form.
**Learning:** Enforcing SECRET_KEY presence in a ProductionConfig class by raising an error at the class level can prevent the application from starting even in non-production environments if the configuration module is imported. Using a property or a lazy-loading mechanism is safer.
**Prevention:** Use standardized configuration management that defaults to safe development values but mandates environment variables for production. Always enable CSRF protection for browser-facing forms.
