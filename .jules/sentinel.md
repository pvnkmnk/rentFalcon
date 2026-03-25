## 2025-05-15 - Strict Environment Variable Validation and CSRF
**Vulnerability:** Lack of CSRF protection on main search form and hardcoded insecure SECRET_KEY.
**Learning:** Strict validation of environment variables (like SECRET_KEY) during module import can cause unexpected failures in development/test environments if they are only required for production.
**Prevention:** Use @property decorators in Flask configuration classes to implement lazy evaluation of required environment variables. This ensures the application can still be imported for testing or development without setting every production secret, while still failing securely if those secrets are missing when actually accessed.
