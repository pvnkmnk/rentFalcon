## 2026-03-19 - [Configuration validation challenges]
**Vulnerability:** Hardcoded SECRET_KEY in app.py.
**Learning:** Initial attempts to move configuration to a centralized config.py revealed that strict validation in the ProductionConfig class (e.g., raising ValueError if SECRET_KEY is missing) can prevent the application from even importing the configuration module if environment variables are missing during the build or initialization phase.
**Prevention:** Use properties for sensitive configuration values that require validation. This ensures validation occurs only when the value is actually accessed, rather than at module import time, allowing for more flexible initialization and error handling.
