from uuid import UUID
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class PengaduanCreate(BaseModel):
    penduduk_id: UUID
    rt_id: UUID | None = None

    kategori: str | None = None
    judul: str
    deskripsi: str

    lokasi: str | None = None
    latitude: Decimal | None = Field(default=None, ge=-90, le=90)
    longitude: Decimal | None = Field(default=None, ge=-180, le=180)


class PengaduanUpdate(BaseModel):
    rt_id: UUID | None = None

    kategori: str | None = None
    judul: str | None = None
    deskripsi: str | None = None

    lokasi: str | None = None
    latitude: Decimal | None = Field(default=None, ge=-90, le=90)
    longitude: Decimal | None = Field(default=None, ge=-180, le=180)

    status: str | None = None


class PengaduanResponse(BaseModel):
    id: UUID
    penduduk_id: UUID
    rt_id: UUID | None = None

    nomor_pengaduan: str | None = None
    kategori: str | None = None
    judul: str
    deskripsi: str

    lokasi: str | None = None
    latitude: Decimal | None = None
    longitude: Decimal | None = None

    status: str | None = None

    created_at: datetime | None = None
    updated_at: datetime | None = None
    selesai_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
