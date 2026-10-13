from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class BeritaCreate(BaseModel):
    judul: str = Field(min_length=1, max_length=200)
    konten: str = Field(min_length=1)
    thumbnail: str | None = Field(default=None, max_length=255)
    author_id: UUID | None = None
    status: str = "draft"


class BeritaUpdate(BaseModel):
    judul: str | None = Field(default=None, min_length=1, max_length=200)
    konten: str | None = Field(default=None, min_length=1)
    thumbnail: str | None = Field(default=None, max_length=255)
    status: str | None = None


class BeritaResponse(BaseModel):
    id: UUID
    judul: str | None = None
    slug: str | None = None
    konten: str | None = None
    thumbnail: str | None = None
    author_id: UUID | None = None
    status: str | None = None
    published_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class PengumumanCreate(BaseModel):
    judul: str = Field(min_length=1, max_length=200)
    konten: str = Field(min_length=1)
    author_id: UUID | None = None
    status: str = "draft"


class PengumumanUpdate(BaseModel):
    judul: str | None = Field(default=None, min_length=1, max_length=200)
    konten: str | None = Field(default=None, min_length=1)
    status: str | None = None


class PengumumanResponse(BaseModel):
    id: UUID
    judul: str | None = None
    konten: str | None = None
    author_id: UUID | None = None
    status: str | None = None
    published_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
