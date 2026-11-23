from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

from database import Base


def _now():
    return datetime.now(timezone.utc)


class GalleryItem(Base):
    __tablename__ = "gallery_items"
    id = Column(Integer, primary_key=True)
    public_id = Column(String(255), unique=True, nullable=False)
    url = Column(String(500), nullable=False)          # Cloudinary secure_url
    resource_type = Column(String(20), default="image")  # image | video
    caption = Column(String(200), default="")
    created_at = Column(DateTime(timezone=True), default=_now)


class ContactMessage(Base):
    __tablename__ = "contact_messages"
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    email = Column(String(200), nullable=False)
    phone = Column(String(40), default="")
    subject = Column(String(200), nullable=False)
    message = Column(Text, default="")
    handled = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=_now)
