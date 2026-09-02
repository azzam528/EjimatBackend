import uuid
from sqlalchemy import Column, String, ForeignKey, Text, DateTime, Date, Numeric, Uuid
from sqlalchemy.orm import relationship
from app.database.base import Base

class Pembangunan(Base):
    __tablename__ = "pembangunan"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    nama_proyek = Column(String(200))
    deskripsi = Column(Text)
    lokasi = Column(Text)
    rt_id = Column(ForeignKey("rt.id"))
    anggaran = Column(Numeric(15, 2))
    tanggal_mulai = Column(Date)
    target_selesai = Column(Date)
    tanggal_selesai = Column(Date)
    progress = Column(Numeric(5, 2))
    status = Column(String(30))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    rt = relationship("RT", back_populates="pembangunan")
    dokumentasi_pembangunan = relationship("DokumentasiPembangunan", back_populates="pembangunan")

class DokumentasiPembangunan(Base):
    __tablename__ = "dokumentasi_pembangunan"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    pembangunan_id = Column(ForeignKey("pembangunan.id"))
    file_path = Column(String(255))
    deskripsi = Column(Text)
    uploaded_at = Column(DateTime)

    pembangunan = relationship("Pembangunan", back_populates="dokumentasi_pembangunan")
