from sqlalchemy import Column, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel

class Dusun(BaseModel):
    __tablename__ = "dusun"

    nama = Column(String(100), nullable=False)

    rws = relationship("RW", back_populates="dusun")
    pembangunans = relationship("Pembangunan", back_populates="dusun")
    pengurus = relationship("PengurusWilayah", back_populates="dusun")

class RW(BaseModel):
    __tablename__ = "rw"

    nama = Column(String(50), nullable=False)
    dusun_id = Column(ForeignKey("dusun.id"), nullable=False)

    dusun = relationship("Dusun", back_populates="rws")
    rts = relationship("RT", back_populates="rw")
    pengurus = relationship("PengurusWilayah", back_populates="rw")

class RT(BaseModel):
    __tablename__ = "rt"

    nama = Column(String(50), nullable=False)
    rw_id = Column(ForeignKey("rw.id"), nullable=False)

    rw = relationship("RW", back_populates="rts")
    kartu_keluargas = relationship("KartuKeluarga", back_populates="rt")
    pengurus = relationship("PengurusWilayah", back_populates="rt")

class PengurusWilayah(BaseModel):
    __tablename__ = "pengurus_wilayah"

    penduduk_id = Column(ForeignKey("penduduk.id"), nullable=False)
    rt_id = Column(ForeignKey("rt.id"), nullable=True)
    rw_id = Column(ForeignKey("rw.id"), nullable=True)
    dusun_id = Column(ForeignKey("dusun.id"), nullable=True)
    jabatan = Column(String(100), nullable=False)
    mulai_menjabat = Column(Date, nullable=False)
    akhir_menjabat = Column(Date, nullable=True)

    penduduk = relationship("Penduduk", back_populates="pengurus")
    rt = relationship("RT", back_populates="pengurus")
    rw = relationship("RW", back_populates="pengurus")
    dusun = relationship("Dusun", back_populates="pengurus")
