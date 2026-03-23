## 2025-05-15 - Lazy SECRET_KEY Validation in ProductionConfig
**Vulnerability:** Eager validation of `SECRET_KEY` in `ProductionConfig` caused `ValueError` during module import, even in non-production environments.
**Learning:** Hard-coded validation in class definitions runs at import time. In Flask projects with multiple config classes, this can block testing or development if production-only secrets are missing from the environment.
**Prevention:** Use `@property` for lazy evaluation of sensitive environment variables in configuration classes, or validate only when the specific configuration is active.
