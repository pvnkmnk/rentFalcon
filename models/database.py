from datetime import datetime
from typing import Optional

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Index, event
from sqlalchemy.engine import Engine
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()


class User(db.Model):
    """User model for multi-user support"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    last_login = db.Column(db.DateTime)

    # Email preferences
    email_notifications = db.Column(db.Boolean, default=True, nullable=False)
    notification_frequency = db.Column(
        db.String(20), default="daily", nullable=False
    )  # 'daily', 'weekly', 'instant'

    # Relationships
    searches = db.relationship(
        "SavedSearch", back_populates="user", cascade="all, delete-orphan"
    )

    def __init__(self, username: str, email: str, password: str):
        self.username = username
        self.email = email
        self.set_password(password)

    def set_password(self, password: str):
        """Hash and set user password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Verify password against hash"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"


class SavedSearch(db.Model):
    """Saved search configurations"""

    __tablename__ = "saved_searches"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    min_price = db.Column(db.Integer)
    max_price = db.Column(db.Integer)

    # Search preferences
    enabled_sources = db.Column(
        db.String(500), default="kijiji,realtor,rentals,viewit,apartments"
    )
    min_bedrooms = db.Column(db.Integer)
    max_bedrooms = db.Column(db.Integer)
    min_bathrooms = db.Column(db.Float)

    # Scheduling
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    schedule_enabled = db.Column(db.Boolean, default=False, nullable=False)
    schedule_frequency = db.Column(
        db.String(20), default="daily"
    )  # 'hourly', 'daily', 'weekly'
    last_run = db.Column(db.DateTime)
    next_run = db.Column(db.DateTime)

    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    user = db.relationship("User", back_populates="searches")

    def get_sources_list(self):
        """Return enabled sources as a list"""
        if self.enabled_sources:
            return [s.strip() for s in self.enabled_sources.split(",")]
        return []

    def __repr__(self):
        return f"<SavedSearch {self.name} - {self.location}>"


class AppSettings(db.Model):
    """Application-wide settings and metadata"""

    __tablename__ = "app_settings"

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    @staticmethod
    def get_setting(key: str, default: Optional[str] = None) -> Optional[str]:
        """Get a setting value"""
        setting = AppSettings.query.filter_by(key=key).first()
        return setting.value if setting else default

    @staticmethod
    def set_setting(key: str, value: str):
        """Set a setting value"""
        setting = AppSettings.query.filter_by(key=key).first()
        if setting:
            setting.value = value
            setting.updated_at = datetime.utcnow()
        else:
            setting = AppSettings(key=key, value=value)
            db.session.add(setting)
        db.session.commit()

    def __repr__(self):
        return f"<AppSettings {self.key}={self.value}>"


# SQLite-specific optimizations
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_conn, connection_record):
    """Enable SQLite optimizations"""
    if "sqlite" in str(dbapi_conn):
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.close()


def init_db(app):
    """Initialize the database"""
    db.init_app(app)

    with app.app_context():
        db.create_all()


def create_default_user():
    """Create a default user for single-user mode"""
    existing_user = User.query.first()
    if not existing_user:
        default_user = User(
            username="admin", email="admin@localhost", password="changeme"
        )
        db.session.add(default_user)
        db.session.commit()
        return default_user
    return existing_user
