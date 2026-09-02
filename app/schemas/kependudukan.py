from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import date, datetime
from typing import Optional

class PendudukBase(BaseModel):
    nik: str
    no_kk: str
    nama_lengkap: str
    tempat_lahir: Optional[str] = None
    tanggal_lahir: Optional[date] = None
    jenis_kelamin: Optional[str] = None
    status_perkawinan: Optional[str] = None
    pendidikan: Optional[str] = None
    pekerjaan: Optional[str] = None
    alamat: Optional[str] = None
    rt_id: UUID
    status_penduduk: Optional[str] = None

class PendudukCreate(PendudukBase):
    pass

class PendudukResponse(PendudukBase):
    id: UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

class KartuKeluargaBase(BaseModel):
    no_kk: str
    kepala_keluarga_id: UUID
    alamat: Optional[str] = None
    rt_id: UUID

class KartuKeluargaCreate(KartuKeluargaBase):
    pass

class KartuKeluargaResponse(KartuKeluargaBase):
    id: UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)
