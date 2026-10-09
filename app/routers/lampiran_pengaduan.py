```python
from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
    status,
)
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.lampiran_pengaduan import (
    LampiranPengaduanResponse,
)
from app.services.lampiran_pengaduan_service import (
    LampiranPengaduanService,
)


router = APIRouter(tags=["Lampiran Pengaduan"])

service = LampiranPengaduanService()


@router.post(
    "/api/pengaduan/{pengaduan_id}/lampiran",
    response_model=LampiranPengaduanResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_lampiran(
    pengaduan_id: UUID,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    return await service.upload_lampiran(
        db,
        pengaduan_id,
        file,
    )


@router.get(
    "/api/pengaduan/{pengaduan_id}/lampiran",
    response_model=list[LampiranPengaduanResponse],
)
def list_lampiran(
    pengaduan_id: UUID,
    db: Session = Depends(get_db),
):
    return service.list_lampiran(
        db,
        pengaduan_id,
    )


@router.get(
    "/api/lampiran-pengaduan/{lampiran_id}",
    response_model=LampiranPengaduanResponse,
)
def get_lampiran(
    lampiran_id: UUID,
    db: Session = Depends(get_db),
):
    return service.get_lampiran(
        db,
        lampiran_id,
    )


@router.delete(
    "/api/lampiran-pengaduan/{lampiran_id}",
)
def delete_lampiran(
    lampiran_id: UUID,
    db: Session = Depends(get_db),
):
    return service.delete_lampiran(
        db,
        lampiran_id,
    )
```