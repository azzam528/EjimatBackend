```python
from uuid import UUID
from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class PembangunanCreate(BaseModel):
    nama_proyek: str = Field(min_length=1, max_length=200)
    deskripsi: str | None = None
    lokasi: str | None = None
    rt_id: UUID | None = None
    anggaran: Decimal | None = Field(default=None, ge=0)
    tanggal_mulai: date | None = None
    target_selesai: date | None = None
    tanggal_selesai: date | None = None
    progress: Decimal = Field(default=0, ge=0, le=100)
    status: str = "direncanakan"


class PembangunanUpdate(BaseModel):
    nama_proyek: str | None = Field(default=None, min_length=1, max_length=200)
    deskripsi: str | None = None
    lokasi: str | None = None
    rt_id: UUID | None = None
    anggaran: Decimal | None = Field(default=None, ge=0)
    tanggal_mulai: date | None = None
    target_selesai: date | None = None
    tanggal_selesai: date | None = None
    progress: Decimal | None = Field(default=None, ge=0, le=100)
    status: str | None = None


class PembangunanResponse(BaseModel):
    id: UUID
    nama_proyek: str | None = None
    deskripsi: str | None = None
    lokasi: str | None = None
    rt_id: UUID | None = None
    anggaran: Decimal | None = None
    tanggal_mulai: date | None = None
    target_selesai: date | None = None
    tanggal_selesai: date | None = None
    progress: Decimal | None = None
    status: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
```