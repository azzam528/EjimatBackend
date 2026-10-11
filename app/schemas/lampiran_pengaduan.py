from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class LampiranPengaduanResponse(BaseModel):
    id: UUID
    pengaduan_id: UUID
    file_path: str
    file_type: str | None = None
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
