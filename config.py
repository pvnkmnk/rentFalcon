import os
from datetime import timedelta


class Config:
    """Base configuration class"""

    # Flask Configuration
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key-change-in-production"
    DEBUG = False
    TESTING = False

    # Database Configuration
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL") or "sqlite:///rental_scanner.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    # Application Settings
    APP_NAME = "Rental Scanner"
    APP_VERSION = "2.0.0"

    # Pagination
    LISTINGS_PER_PAGE = 25
    MAX_SEARCH_RESULTS = 100

    # Scraper Configuration
    SCRAPER_TIMEOUT = 30  # seconds
    SCRAPER_MAX_RETRIES = 3
    SCRAPER_DELAY = 1  # seconds between requests
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

    # Enabled Scrapers (can be controlled via environment)
    ENABLED_SCRAPERS = os.environ.get(
        "ENABLED_SCRAPERS", "kijiji,realtor,rentals,viewit,apartments"
    ).split(",")

    # Rate Limiting
    RATE_LIMIT_ENABLED = True
    RATE_LIMIT_PER_SCRAPER = "10 per minute"

    # Cache Configuration (for Redis or simple in-memory)
    CACHE_TYPE = "simple"
    CACHE_DEFAULT_TIMEOUT = 300  # 5 minutes
    CACHE_REDIS_URL = os.environ.get("REDIS_URL")

    # Scheduler Configuration (APScheduler)
    SCHEDULER_API_ENABLED = True
    SCHEDULER_TIMEZONE = "America/Toronto"

    # Email Configuration
    MAIL_ENABLED = os.environ.get("MAIL_ENABLED", "false").lower() == "true"
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "true").lower() == "true"
    MAIL_USE_SSL = os.environ.get("MAIL_USE_SSL", "false").lower() == "true"
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get(
        "MAIL_DEFAULT_SENDER", "noreply@rentalscanner.local"
    )

    # Report Configuration
    REPORT_FREQUENCY_OPTIONS = ["daily", "weekly", "manual"]
    REPORT_MAX_LISTINGS = 50

    # Listing Expiry
    LISTING_EXPIRY_DAYS = int(os.environ.get("LISTING_EXPIRY_DAYS", 7))

    # Multi-User Configuration
    MULTI_USER_ENABLED = os.environ.get("MULTI_USER_ENABLED", "false").lower() == "true"
    REQUIRE_LOGIN = os.environ.get("REQUIRE_LOGIN", "false").lower() == "true"
    MAX_SAVED_SEARCHES_PER_USER = int(os.environ.get("MAX_SAVED_SEARCHES_PER_USER", 10))

    # Session Configuration
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    # Logging
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
    LOG_FILE = os.environ.get("LOG_FILE", "rental_scanner.log")
    LOG_MAX_BYTES = 10485760  # 10MB
    LOG_BACKUP_COUNT = 5

    # Debug Options
    SAVE_DEBUG_HTML = os.environ.get("SAVE_DEBUG_HTML", "false").lower() == "true"
    DEBUG_OUTPUT_DIR = "debug_output"

    # API Keys (for services that have them)
    FACEBOOK_ACCESS_TOKEN = os.environ.get("FACEBOOK_ACCESS_TOKEN")
    RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY")  # For unofficial APIs

    # Security
    BCRYPT_LOG_ROUNDS = 12
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None


class DevelopmentConfig(Config):
    """Development environment configuration"""

    DEBUG = True
    SQLALCHEMY_ECHO = False
    SAVE_DEBUG_HTML = True
    CACHE_TYPE = "simple"
    MAIL_ENABLED = False
    RATE_LIMIT_ENABLED = False


class ProductionConfig(Config):
    """Production environment configuration"""

    DEBUG = False
    TESTING = False

    # Force HTTPS in production
    SESSION_COOKIE_SECURE = True

    # Use Redis for caching in production
    CACHE_TYPE = "redis" if Config.CACHE_REDIS_URL else "simple"

    # Production should have real secret key
    SECRET_KEY = os.environ.get("SECRET_KEY")
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable must be set in production")

    # Production logging
    LOG_LEVEL = "WARNING"
    SQLALCHEMY_ECHO = False
    SAVE_DEBUG_HTML = False


class TestingConfig(Config):
    """Testing environment configuration"""

    TESTING = True
    DEBUG = True

    # Use in-memory database for tests
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

    # Disable CSRF for testing
    WTF_CSRF_ENABLED = False

    # Disable email in tests
    MAIL_ENABLED = False

    # Disable rate limiting in tests
    RATE_LIMIT_ENABLED = False

    # Fast scraping for tests
    SCRAPER_TIMEOUT = 5
    SCRAPER_DELAY = 0


class DockerConfig(ProductionConfig):
    """Docker deployment configuration"""

    # Database will be PostgreSQL in Docker
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL")
        or "postgresql://rental_user:rental_pass@db:5432/rental_scanner"
    )

    # Redis will be available in Docker
    CACHE_TYPE = "redis"
    CACHE_REDIS_URL = os.environ.get("REDIS_URL") or "redis://redis:6379/0"

    # Enable multi-user by default in Docker
    MULTI_USER_ENABLED = True
    REQUIRE_LOGIN = True


# Configuration dictionary
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "docker": DockerConfig,
    "default": DevelopmentConfig,
}


def get_config():
    """Get configuration based on environment variable"""
    env = os.environ.get("FLASK_ENV", "development")
    return config.get(env, config["default"])
