import uuid
from sqlalchemy import Column, String, ForeignKey, Text, DateTime, Date, Uuid
from sqlalchemy.orm import relationship
from app.database.base import Base

class Penduduk(Base):
    __tablename__ = "penduduk"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    nik = Column(String(16))
    no_kk = Column(String(16))
    nama_lengkap = Column(String(150))
    tempat_lahir = Column(String(100))
    tanggal_lahir = Column(Date)
    jenis_kelamin = Column(String(20))
    status_perkawinan = Column(String(30))
    pendidikan = Column(String(100))
    pekerjaan = Column(String(100))
    alamat = Column(Text)
    rt_id = Column(ForeignKey("rt.id"))
    status_penduduk = Column(String(30))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    rt = relationship("RT", back_populates="penduduk")
    anggota_keluarga = relationship("AnggotaKeluarga", back_populates="penduduk")
    pengajuan_layanan = relationship("PengajuanLayanan", back_populates="penduduk")
    pengaduan = relationship("Pengaduan", back_populates="penduduk")

class KartuKeluarga(Base):
    __tablename__ = "kartu_keluarga"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    no_kk = Column(String(16))
    kepala_keluarga_id = Column(ForeignKey("penduduk.id"))
    alamat = Column(Text)
    rt_id = Column(ForeignKey("rt.id"))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    rt = relationship("RT", back_populates="kartu_keluarga")
    kepala_keluarga = relationship("Penduduk", foreign_keys=[kepala_keluarga_id])
    anggota_keluarga = relationship("AnggotaKeluarga", back_populates="kartu_keluarga")

class AnggotaKeluarga(Base):
    __tablename__ = "anggota_keluarga"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    kk_id = Column(ForeignKey("kartu_keluarga.id"))
    penduduk_id = Column(ForeignKey("penduduk.id"))
    hubungan_keluarga = Column(String(50))
    created_at = Column(DateTime)

    kartu_keluarga = relationship("KartuKeluarga", back_populates="anggota_keluarga")
    penduduk = relationship("Penduduk", back_populates="anggota_keluarga")
