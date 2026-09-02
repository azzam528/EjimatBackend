import uuid
from sqlalchemy import Column, String, ForeignKey, DateTime, Date, Boolean, Uuid
from sqlalchemy.orm import relationship
from app.database.base import Base

class Dusun(Base):
    __tablename__ = "dusun"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    name = Column(String(100))
    code = Column(String(20))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    rws = relationship("RW", back_populates="dusun")
    pengurus = relationship("PengurusWilayah", back_populates="dusun")

class RW(Base):
    __tablename__ = "rw"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    dusun_id = Column(ForeignKey("dusun.id"))
    number = Column(String(10))
    code = Column(String(20))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    dusun = relationship("Dusun", back_populates="rws")
    rts = relationship("RT", back_populates="rw")
    pengurus = relationship("PengurusWilayah", back_populates="rw")

class RT(Base):
    __tablename__ = "rt"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    rw_id = Column(ForeignKey("rw.id"))
    number = Column(String(10))
    code = Column(String(20))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    rw = relationship("RW", back_populates="rts")
    penduduk = relationship("Penduduk", back_populates="rt")
    kartu_keluarga = relationship("KartuKeluarga", back_populates="rt")
    pengurus = relationship("PengurusWilayah", back_populates="rt")
    pengaduan = relationship("Pengaduan", back_populates="rt")
    pembangunan = relationship("Pembangunan", back_populates="rt")

class PengurusWilayah(Base):
    __tablename__ = "pengurus_wilayah"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id = Column(ForeignKey("users.id"))
    dusun_id = Column(ForeignKey("dusun.id"), nullable=True)
    rw_id = Column(ForeignKey("rw.id"), nullable=True)
    rt_id = Column(ForeignKey("rt.id"), nullable=True)
    jabatan = Column(String(50))
    periode_mulai = Column(Date)
    periode_selesai = Column(Date)
    is_active = Column(Boolean)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    user = relationship("User", back_populates="pengurus_wilayah")
    dusun = relationship("Dusun", back_populates="pengurus")
    rw = relationship("RW", back_populates="pengurus")
    rt = relationship("RT", back_populates="pengurus")
