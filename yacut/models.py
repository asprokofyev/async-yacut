from datetime import datetime, timezone
from yacut import db
from yacut.constants import MAX_CUSTOM_SHORT_ID_LENGTH, MAX_ORIGINAL_URL_LENGTH


class URLMap(db.Model):  # type: ignore[name-defined]
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(
        db.String(MAX_ORIGINAL_URL_LENGTH),
        nullable=False
    )
    short = db.Column(
        db.String(MAX_CUSTOM_SHORT_ID_LENGTH),
        unique=True,
        nullable=False,
        index=True
    )
    timestamp = db.Column(
        db.DateTime, index=True, default=lambda: datetime.now(timezone.utc)
    )
