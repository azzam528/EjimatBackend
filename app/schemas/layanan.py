from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional


class JenisLayananBase(BaseModel):
    nama_layanan: str
    deskripsi: Optional[str] = None
    persyaratan: Optional[str] = None
    template_surat: Optional[str] = None
    is_active: bool = True


class JenisLayananCreate(JenisLayananBase):
    pass


class JenisLayananUpdate(BaseModel):
    nama_layanan: Optional[str] = None
    deskripsi: Optional[str] = None
    persyaratan: Optional[str] = None
    template_surat: Optional[str] = None
    is_active: Optional[bool] = None


class JenisLayananResponse(JenisLayananBase):
    id: UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class PengajuanLayananBase(BaseModel):
    jenis_layanan_id: UUID
    penduduk_id: UUID
    catatan_pemohon: Optional[str] = None


class PengajuanLayananCreate(PengajuanLayananBase):
    pass


class PengajuanLayananUpdate(BaseModel):
    status: Optional[str] = None
    catatan_petugas: Optional[str] = None


class PengajuanLayananResponse(PengajuanLayananBase):
    id: UUID
    nomor_pengajuan: str
    status: str
    catatan_petugas: Optional[str] = None
    diajukan_at: Optional[datetime] = None
    selesai_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)