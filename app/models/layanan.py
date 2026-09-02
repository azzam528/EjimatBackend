import uuid
from sqlalchemy import Column, String, ForeignKey, Text, DateTime, Boolean, BigInteger, Uuid
from sqlalchemy.orm import relationship
from app.database.base import Base

class JenisLayanan(Base):
    __tablename__ = "jenis_layanan"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    nama_layanan = Column(String(150))
    deskripsi = Column(Text)
    persyaratan = Column(Text)
    template_surat = Column(String(255))
    is_active = Column(Boolean)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    pengajuan_layanan = relationship("PengajuanLayanan", back_populates="jenis_layanan")

class PengajuanLayanan(Base):
    __tablename__ = "pengajuan_layanan"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    jenis_layanan_id = Column(ForeignKey("jenis_layanan.id"))
    penduduk_id = Column(ForeignKey("penduduk.id"))
    nomor_pengajuan = Column(String(50))
    status = Column(String(30))
    catatan_pemohon = Column(Text)
    catatan_petugas = Column(Text)
    diajukan_at = Column(DateTime)
    selesai_at = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    jenis_layanan = relationship("JenisLayanan", back_populates="pengajuan_layanan")
    penduduk = relationship("Penduduk", back_populates="pengajuan_layanan")
    dokumen_pengajuan = relationship("DokumenPengajuan", back_populates="pengajuan_layanan")

class DokumenPengajuan(Base):
    __tablename__ = "dokumen_pengajuan"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    pengajuan_id = Column(ForeignKey("pengajuan_layanan.id"))
    nama_dokumen = Column(String(150))
    file_path = Column(String(255))
    file_type = Column(String(50))
    file_size = Column(BigInteger)
    uploaded_at = Column(DateTime)

    pengajuan_layanan = relationship("PengajuanLayanan", back_populates="dokumen_pengajuan")
