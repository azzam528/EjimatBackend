from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional

class DusunBase(BaseModel):
    name: str
    code: Optional[str] = None

class DusunCreate(DusunBase):
    pass

class DusunResponse(DusunBase):
    id: UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

class RWBase(BaseModel):
    dusun_id: UUID
    number: str
    code: Optional[str] = None

class RWCreate(RWBase):
    pass

class RWResponse(RWBase):
    id: UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

class RTBase(BaseModel):
    rw_id: UUID
    number: str
    code: Optional[str] = None

class RTCreate(RTBase):
    pass

class RTResponse(RTBase):
    id: UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)
