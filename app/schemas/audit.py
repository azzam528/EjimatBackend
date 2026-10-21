from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AuditLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID | None
    action: str | None
    module: str | None
    table_name: str | None
    record_id: UUID | None
    old_data: str | None
    new_data: str | None
    ip_address: str | None
    created_at: datetime | None
