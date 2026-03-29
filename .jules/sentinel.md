## 2026-03-29 - [Security Improvement] Add CSRF protection and harden SECRET_KEY

**Vulnerability:**
1. Missing CSRF protection on the main rental search form allowed for potential cross-site request forgery attacks.
2. Hardcoded `SECRET_KEY` in `app.py` posed a risk of sensitive data exposure if the codebase is made public.

**Learning:**
Standardizing the security configuration directly in the entry point `app.py` is necessary when the application handles sensitive operations like search forms, especially as a multi-source rental aggregator.

**Prevention:**
Always initialize `CSRFProtect` in the Flask application and load all sensitive secrets from environment variables with safe fallbacks only for development. Ensure that all state-changing endpoints (POST/PUT/DELETE) have CSRF protection or are explicitly exempted with a clear justification.
