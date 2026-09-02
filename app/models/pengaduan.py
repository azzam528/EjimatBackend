from sqlalchemy import Column, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel

class Pengaduan(BaseModel):
    __tablename__ = "pengaduan"

    penduduk_id = Column(ForeignKey("penduduk.id"), nullable=False)
    judul = Column(String(200), nullable=False)
    deskripsi = Column(Text, nullable=False)
    status = Column(String(50), nullable=False)
    tanggal_pengaduan = Column(DateTime(timezone=True), nullable=False)

    penduduk = relationship("Penduduk", back_populates="pengaduan")
    lampiran_pengaduan = relationship("LampiranPengaduan", back_populates="pengaduan")

class LampiranPengaduan(BaseModel):
    __tablename__ = "lampiran_pengaduan"

    pengaduan_id = Column(ForeignKey("pengaduan.id"), nullable=False)
    file_path = Column(String(255), nullable=False)

    pengaduan = relationship("Pengaduan", back_populates="lampiran_pengaduan")
