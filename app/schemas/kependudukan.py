from pydantic import BaseModel, ConfigDict, field_validator
from uuid import UUID
from datetime import date, datetime
from typing import Optional

class PendudukBase(BaseModel):
    nik: Optional[str] = None
    no_kk: Optional[str] = None
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

    @field_validator("nik", "no_kk")
    @classmethod
    def validate_sixteen_digits(cls, value: Optional[str]) -> Optional[str]:
        if value is not None and (len(value) != 16 or not value.isdigit()):
            raise ValueError("must contain exactly 16 digits")
        return value

    @field_validator("nama_lengkap")
    @classmethod
    def validate_nama_lengkap(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("nama_lengkap must not be empty")
        return value

class PendudukCreate(PendudukBase):
    pass

class PendudukUpdate(BaseModel):
    nik: Optional[str] = None
    no_kk: Optional[str] = None
    nama_lengkap: Optional[str] = None
    tempat_lahir: Optional[str] = None
    tanggal_lahir: Optional[date] = None
    jenis_kelamin: Optional[str] = None
    status_perkawinan: Optional[str] = None
    pendidikan: Optional[str] = None
    pekerjaan: Optional[str] = None
    alamat: Optional[str] = None
    rt_id: Optional[UUID] = None
    status_penduduk: Optional[str] = None

    @field_validator("nik", "no_kk")
    @classmethod
    def validate_sixteen_digits(cls, value: Optional[str]) -> Optional[str]:
        if value is not None and (len(value) != 16 or not value.isdigit()):
            raise ValueError("must contain exactly 16 digits")
        return value

    @field_validator("nama_lengkap")
    @classmethod
    def validate_nama_lengkap(cls, value: Optional[str]) -> Optional[str]:
        if value is not None and not value.strip():
            raise ValueError("nama_lengkap must not be empty")
        return value

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
