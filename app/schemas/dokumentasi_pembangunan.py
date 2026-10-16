from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DokumentasiPembangunanResponse(BaseModel):
    id: UUID
    pembangunan_id: UUID
    file_path: str | None = None
    deskripsi: str | None = None
    uploaded_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)