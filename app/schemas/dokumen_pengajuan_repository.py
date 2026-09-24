from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DokumenPengajuanResponse(BaseModel):
    id: UUID
    pengajuan_id: UUID
    nama_dokumen: str
    file_path: str
    file_type: str | None = None
    file_size: int | None = None
    uploaded_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)