from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime

class DusunBase(BaseModel):
    nama: str

class DusunCreate(DusunBase):
    pass

class DusunResponse(DusunBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class RWBase(BaseModel):
    nama: str
    dusun_id: UUID

class RWCreate(RWBase):
    pass

class RWResponse(RWBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class RTBase(BaseModel):
    nama: str
    rw_id: UUID

class RTCreate(RTBase):
    pass

class RTResponse(RTBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
