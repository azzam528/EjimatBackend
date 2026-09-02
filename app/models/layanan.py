from sqlalchemy import Column, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel

class JenisLayanan(BaseModel):
    __tablename__ = "jenis_layanan"

    nama = Column(String(100), nullable=False)
    deskripsi = Column(Text)

    pengajuan_layanan = relationship("PengajuanLayanan", back_populates="jenis_layanan")

class PengajuanLayanan(BaseModel):
    __tablename__ = "pengajuan_layanan"

    penduduk_id = Column(ForeignKey("penduduk.id"), nullable=False)
    jenis_layanan_id = Column(ForeignKey("jenis_layanan.id"), nullable=False)
    status = Column(String(50), nullable=False)
    tanggal_pengajuan = Column(DateTime(timezone=True), nullable=False)
    keterangan = Column(Text)

    penduduk = relationship("Penduduk", back_populates="pengajuan_layanan")
    jenis_layanan = relationship("JenisLayanan", back_populates="pengajuan_layanan")
    dokumen_pengajuan = relationship("DokumenPengajuan", back_populates="pengajuan_layanan")

class DokumenPengajuan(BaseModel):
    __tablename__ = "dokumen_pengajuan"

    pengajuan_layanan_id = Column(ForeignKey("pengajuan_layanan.id"), nullable=False)
    nama_dokumen = Column(String(100), nullable=False)
    file_path = Column(String(255), nullable=False)

    pengajuan_layanan = relationship("PengajuanLayanan", back_populates="dokumen_pengajuan")
