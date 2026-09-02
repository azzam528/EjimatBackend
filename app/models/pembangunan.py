from sqlalchemy import Column, String, ForeignKey, Text, Date, Numeric
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel

class Pembangunan(BaseModel):
    __tablename__ = "pembangunan"

    nama_proyek = Column(String(200), nullable=False)
    deskripsi = Column(Text)
    anggaran = Column(Numeric(15, 2))
    status = Column(String(50), nullable=False)
    tanggal_mulai = Column(Date)
    tanggal_selesai = Column(Date)
    dusun_id = Column(ForeignKey("dusun.id"), nullable=False)

    dusun = relationship("Dusun", back_populates="pembangunans")
    dokumentasi_pembangunan = relationship("DokumentasiPembangunan", back_populates="pembangunan")

class DokumentasiPembangunan(BaseModel):
    __tablename__ = "dokumentasi_pembangunan"

    pembangunan_id = Column(ForeignKey("pembangunan.id"), nullable=False)
    file_path = Column(String(255), nullable=False)
    keterangan = Column(Text)

    pembangunan = relationship("Pembangunan", back_populates="dokumentasi_pembangunan")
