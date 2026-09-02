from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import date, datetime
from typing import Optional

class PendudukBase(BaseModel):
    nik: str
    nama: str
    tempat_lahir: str
    tanggal_lahir: date
    jenis_kelamin: str
    agama: str
    pekerjaan: Optional[str] = None
    status_perkawinan: str

class PendudukCreate(PendudukBase):
    pass

class PendudukResponse(PendudukBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class KartuKeluargaBase(BaseModel):
    nomor_kk: str
    rt_id: UUID
    alamat: str

class KartuKeluargaCreate(KartuKeluargaBase):
    pass

class KartuKeluargaResponse(KartuKeluargaBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
