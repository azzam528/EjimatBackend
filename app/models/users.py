from sqlalchemy import Column, String, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel

class Role(BaseModel):
    __tablename__ = "roles"

    name = Column(String(50), nullable=False, unique=True)
    description = Column(String(255))

    users = relationship("User", back_populates="role")


class User(BaseModel):
    __tablename__ = "users"

    username = Column(String(50), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    role_id = Column(ForeignKey("roles.id"), nullable=False)
    is_active = Column(Boolean, default=True)

    role = relationship("Role", back_populates="users")
    audit_logs = relationship("AuditLog", back_populates="user")
    berita = relationship("Berita", back_populates="penulis")


class AuditLog(BaseModel):
    __tablename__ = "audit_logs"

    user_id = Column(ForeignKey("users.id"), nullable=True)
    action = Column(String(50), nullable=False)
    table_name = Column(String(50), nullable=False)
    record_id = Column(String(50), nullable=False)
    details = Column(JSON, nullable=True)

    user = relationship("User", back_populates="audit_logs")
