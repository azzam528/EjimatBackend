import uuid
from sqlalchemy import Column, String, ForeignKey, Text, DateTime, Numeric, Uuid
from sqlalchemy.orm import relationship
from app.database.base import Base

class Pengaduan(Base):
    __tablename__ = "pengaduan"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    penduduk_id = Column(ForeignKey("penduduk.id"))
    rt_id = Column(ForeignKey("rt.id"))
    nomor_pengaduan = Column(String(50))
    kategori = Column(String(100))
    judul = Column(String(200))
    deskripsi = Column(Text)
    lokasi = Column(Text)
    latitude = Column(Numeric(10, 7))
    longitude = Column(Numeric(10, 7))
    status = Column(String(30))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    selesai_at = Column(DateTime)

    penduduk = relationship("Penduduk", back_populates="pengaduan")
    rt = relationship("RT", back_populates="pengaduan")
    lampiran_pengaduan = relationship("LampiranPengaduan", back_populates="pengaduan")

class LampiranPengaduan(Base):
    __tablename__ = "lampiran_pengaduan"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    pengaduan_id = Column(ForeignKey("pengaduan.id"))
    file_path = Column(String(255))
    file_type = Column(String(50))
    created_at = Column(DateTime)

    pengaduan = relationship("Pengaduan", back_populates="lampiran_pengaduan")
