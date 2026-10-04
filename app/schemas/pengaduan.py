from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PengaduanCreate(BaseModel):
    penduduk_id: UUID
    judul: str
    deskripsi: str


class PengaduanUpdate(BaseModel):
    status: str | None = None
    catatan_petugas: str | None = None


class PengaduanResponse(BaseModel):
    id: UUID
    penduduk_id: UUID
    judul: str
    deskripsi: str
    status: str
    tanggal_pengaduan: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
