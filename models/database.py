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
    history = db.relationship(
        "SearchHistory", back_populates="search", cascade="all, delete-orphan"
    )

    def get_sources_list(self):
        """Return enabled sources as a list"""
        if self.enabled_sources:
            return [s.strip() for s in self.enabled_sources.split(",")]
        return []

    def __repr__(self):
        return f"<SavedSearch {self.name} - {self.location}>"


class Listing(db.Model):
    """Rental listing data"""

    __tablename__ = "listings"

    id = db.Column(db.Integer, primary_key=True)

    # Source information
    source = db.Column(db.String(50), nullable=False, index=True)
    external_id = db.Column(db.String(255), nullable=False)
    url = db.Column(db.Text, nullable=False, unique=True)

    # Basic information
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False, index=True)
    location = db.Column(db.String(255), nullable=False, index=True)

    # Property details
    bedrooms = db.Column(db.Integer, index=True)
    bathrooms = db.Column(db.Float)
    square_feet = db.Column(db.Integer)
    property_type = db.Column(db.String(50))  # apartment, house, condo, etc.

    # Media
    image_url = db.Column(db.Text)

    # Dates and tracking
    posted_date = db.Column(db.DateTime, index=True)
    first_seen = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    scraped_at = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False, index=True
    )

    # Status tracking
    status = db.Column(
        db.String(20), default="active", nullable=False, index=True
    )  # 'active', 'expired', 'removed'

    # Price history tracking
    original_price = db.Column(db.Float)
    price_changed = db.Column(db.Boolean, default=False)
    price_change_count = db.Column(db.Integer, default=0)

    # Relationships
    history = db.relationship(
        "ListingHistory", back_populates="listing", cascade="all, delete-orphan"
    )

    # Composite unique index on source and external_id
    __table_args__ = (
        Index("idx_source_external_id", "source", "external_id"),
        Index("idx_location_price", "location", "price"),
        Index("idx_status_last_seen", "status", "last_seen"),
    )

    def mark_as_seen(self):
        """Update the last_seen timestamp"""
        self.last_seen = datetime.utcnow()
        self.status = "active"

    def mark_as_expired(self):
        """Mark listing as expired"""
        self.status = "expired"

    def update_price(self, new_price: float):
        """Update price and track the change"""
        if self.price != new_price:
            if self.original_price is None:
                self.original_price = self.price

            self.price = new_price
            self.price_changed = True
            self.price_change_count += 1

            # Create history entry
            history_entry = ListingHistory(
                listing_id=self.id,
                change_type="price_change",
                old_value=str(self.original_price or self.price),
                new_value=str(new_price),
            )
            self.history.append(history_entry)

    def to_dict(self):
        """Convert listing to dictionary"""
        return {
            "id": self.id,
            "source": self.source,
            "external_id": self.external_id,
            "url": self.url,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "location": self.location,
            "bedrooms": self.bedrooms,
            "bathrooms": self.bathrooms,
            "square_feet": self.square_feet,
            "property_type": self.property_type,
            "image_url": self.image_url,
            "posted_date": self.posted_date.isoformat() if self.posted_date else None,
            "first_seen": self.first_seen.isoformat() if self.first_seen else None,
            "last_seen": self.last_seen.isoformat() if self.last_seen else None,
            "status": self.status,
            "price_changed": self.price_changed,
            "original_price": self.original_price,
        }

    def __repr__(self):
        return f"<Listing {self.source}:{self.external_id} - ${self.price}>"


class ListingHistory(db.Model):
    """Track changes to listings over time"""

    __tablename__ = "listing_history"

    id = db.Column(db.Integer, primary_key=True)
    listing_id = db.Column(db.Integer, db.ForeignKey("listings.id"), nullable=False)

    # Change tracking
    change_type = db.Column(
        db.String(50), nullable=False
    )  # 'price_change', 'status_change', 'update'
    old_value = db.Column(db.Text)
    new_value = db.Column(db.Text)
    change_date = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False, index=True
    )

    # Relationships
    listing = db.relationship("Listing", back_populates="history")

    def __repr__(self):
        return f"<ListingHistory {self.change_type} - Listing {self.listing_id}>"


class SearchHistory(db.Model):
    """Track search executions and results"""

    __tablename__ = "search_history"

    id = db.Column(db.Integer, primary_key=True)
    search_id = db.Column(
        db.Integer, db.ForeignKey("saved_searches.id"), nullable=False
    )

    # Execution details
    executed_at = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False, index=True
    )
    duration_seconds = db.Column(db.Float)
    success = db.Column(db.Boolean, default=True, nullable=False)
    error_message = db.Column(db.Text)

    # Results summary
    total_results = db.Column(db.Integer, default=0)
    new_results = db.Column(db.Integer, default=0)
    results_by_source = db.Column(db.Text)  # JSON string

    # Relationships
    search = db.relationship("SavedSearch", back_populates="history")

    def __repr__(self):
        return f"<SearchHistory {self.executed_at} - {self.total_results} results>"


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
