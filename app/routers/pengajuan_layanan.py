from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.schemas.layanan import (
    PengajuanLayananCreate,
    PengajuanLayananResponse,
    PengajuanLayananUpdate,
)

from app.services.pengajuan_layanan_service import (
    PengajuanLayananService,
)

router = APIRouter(prefix="/api/pengajuan-layanan", tags=["Pengajuan Layanan"])

service = PengajuanLayananService()


@router.get("", response_model=list[PengajuanLayananResponse])
def list_pengajuan_layanan(
    jenis_layanan_id: UUID | None = None,
    penduduk_id: UUID | None = None,
    status: str | None = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    db: Session = Depends(get_db),
):

    return service.list_pengajuan_layanan(
        db,
        jenis_layanan_id=jenis_layanan_id,
        penduduk_id=penduduk_id,
        status=status,
        skip=skip,
        limit=limit,
    )


@router.get("/{pengajuan_id}", response_model=PengajuanLayananResponse)
def get_pengajuan_layanan(pengajuan_id: UUID, db: Session = Depends(get_db)):

    return service.get_pengajuan_layanan(db, pengajuan_id)


@router.post(
    "", response_model=PengajuanLayananResponse, status_code=status.HTTP_201_CREATED
)
def create_pengajuan_layanan(
    data: PengajuanLayananCreate, db: Session = Depends(get_db)
):

    return service.create_pengajuan_layanan(db, data)


@router.put("/{pengajuan_id}", response_model=PengajuanLayananResponse)
def update_pengajuan_layanan(
    pengajuan_id: UUID, data: PengajuanLayananUpdate, db: Session = Depends(get_db)
):

    return service.update_pengajuan_layanan(db, pengajuan_id, data)
