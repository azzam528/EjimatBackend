import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Uuid
from app.database.base import Base

class BaseModel(Base):
    __abstract__ = True

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
