## 2026-03-18 - Configuration Validation Side Effects
**Vulnerability:** Hardcoded SECRET_KEY and missing CSRF protection.
**Learning:** Placing mandatory environment variable checks (e.g., `raise ValueError`) directly in the class body of a configuration class (like `ProductionConfig`) causes the application to crash even in development or testing environments, as the class definition is executed upon import. Moving these checks to a `@property` ensures they only fire when the specific configuration is actually used.
**Prevention:** Use properties or explicit validation methods for runtime environment checks to avoid breaking the application in non-production environments where those variables are not required.
