from sqlalchemy import Column, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel

class Berita(BaseModel):
    __tablename__ = "berita"

    judul = Column(String(200), nullable=False)
    konten = Column(Text, nullable=False)
    penulis_id = Column(ForeignKey("users.id"), nullable=False)
    tanggal_publikasi = Column(DateTime(timezone=True), nullable=False)

    penulis = relationship("User", back_populates="berita")

class Pengumuman(BaseModel):
    __tablename__ = "pengumuman"

    judul = Column(String(200), nullable=False)
    konten = Column(Text, nullable=False)
    tanggal_publikasi = Column(DateTime(timezone=True), nullable=False)
    aktif_sampai = Column(DateTime(timezone=True))
