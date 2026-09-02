import uuid
from sqlalchemy import Column, String, ForeignKey, Text, DateTime, Uuid
from sqlalchemy.orm import relationship
from app.database.base import Base

class Berita(Base):
    __tablename__ = "berita"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    judul = Column(String(200))
    slug = Column(String(220))
    konten = Column(Text)
    thumbnail = Column(String(255))
    author_id = Column(ForeignKey("users.id"))
    status = Column(String(30))
    published_at = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    author = relationship("User", back_populates="berita")

class Pengumuman(Base):
    __tablename__ = "pengumuman"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    judul = Column(String(200))
    konten = Column(Text)
    author_id = Column(ForeignKey("users.id"))
    status = Column(String(30))
    published_at = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    author = relationship("User", back_populates="pengumuman")
