from uuid import UUID

from fastapi import APIRouter, Depends, File, UploadFile, status
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.schemas.dokumen_pengajuan import (
    DokumenPengajuanResponse,
)

from app.services.dokumen_pengajuan_service import (
    DokumenPengajuanService,
)

router = APIRouter(tags=["Dokumen Pengajuan"])

service = DokumenPengajuanService()


@router.post(
    "/api/pengajuan-layanan/{pengajuan_id}/dokumen",
    response_model=DokumenPengajuanResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_dokumen(
    pengajuan_id: UUID,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    return await service.upload_dokumen(
        db,
        pengajuan_id,
        file,
    )


@router.get(
    "/api/pengajuan-layanan/{pengajuan_id}/dokumen",
    response_model=list[DokumenPengajuanResponse],
)
def list_dokumen(
    pengajuan_id: UUID,
    db: Session = Depends(get_db),
):
    return service.list_dokumen(
        db,
        pengajuan_id,
    )


@router.get(
    "/api/dokumen-pengajuan/{dokumen_id}",
    response_model=DokumenPengajuanResponse,
)
def get_dokumen(
    dokumen_id: UUID,
    db: Session = Depends(get_db),
):
    return service.get_dokumen(
        db,
        dokumen_id,
    )


@router.delete(
    "/api/dokumen-pengajuan/{dokumen_id}",
)
def delete_dokumen(
    dokumen_id: UUID,
    db: Session = Depends(get_db),
):
    return service.delete_dokumen(
        db,
        dokumen_id,
    )
