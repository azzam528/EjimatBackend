import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey, Text, DateTime, Uuid
from sqlalchemy.orm import relationship
from app.database.base import Base

class Role(Base):
    __tablename__ = "roles"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    name = Column(String(50), nullable=False)
    description = Column(Text)

    users = relationship("User", back_populates="role")

class User(Base):
    __tablename__ = "users"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    username = Column(String(50), nullable=False)
    email = Column(String(100))
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(150))
    role_id = Column(ForeignKey("roles.id"))
    is_active = Column(Boolean)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    role = relationship("Role", back_populates="users")
    audit_logs = relationship("AuditLog", back_populates="user")
    berita = relationship("Berita", back_populates="author")
    pengumuman = relationship("Pengumuman", back_populates="author")
    pengurus_wilayah = relationship("PengurusWilayah", back_populates="user")

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id = Column(ForeignKey("users.id"))
    action = Column(String(50))
    module = Column(String(100))
    table_name = Column(String(100))
    record_id = Column(Uuid)
    old_data = Column(Text)
    new_data = Column(Text)
    ip_address = Column(String(45))
    created_at = Column(DateTime)

    user = relationship("User", back_populates="audit_logs")
