from sqlalchemy import Column, String, ForeignKey, Date, Text
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel

class KartuKeluarga(BaseModel):
    __tablename__ = "kartu_keluarga"

    nomor_kk = Column(String(20), nullable=False, unique=True)
    rt_id = Column(ForeignKey("rt.id"), nullable=False)
    alamat = Column(Text, nullable=False)

    rt = relationship("RT", back_populates="kartu_keluargas")
    anggota_keluarga = relationship("AnggotaKeluarga", back_populates="kartu_keluarga")

class Penduduk(BaseModel):
    __tablename__ = "penduduk"

    nik = Column(String(16), nullable=False, unique=True)
    nama = Column(String(150), nullable=False)
    tempat_lahir = Column(String(100), nullable=False)
    tanggal_lahir = Column(Date, nullable=False)
    jenis_kelamin = Column(String(20), nullable=False)
    agama = Column(String(50), nullable=False)
    pekerjaan = Column(String(100))
    status_perkawinan = Column(String(50), nullable=False)

    anggota_keluarga = relationship("AnggotaKeluarga", back_populates="penduduk")
    pengurus = relationship("PengurusWilayah", back_populates="penduduk")
    pengajuan_layanan = relationship("PengajuanLayanan", back_populates="penduduk")
    pengaduan = relationship("Pengaduan", back_populates="penduduk")

class AnggotaKeluarga(BaseModel):
    __tablename__ = "anggota_keluarga"

    kartu_keluarga_id = Column(ForeignKey("kartu_keluarga.id"), nullable=False)
    penduduk_id = Column(ForeignKey("penduduk.id"), nullable=False, unique=True)
    status_hubungan = Column(String(50), nullable=False)

    kartu_keluarga = relationship("KartuKeluarga", back_populates="anggota_keluarga")
    penduduk = relationship("Penduduk", back_populates="anggota_keluarga")
