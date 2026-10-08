from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.schemas.pengaduan import (
    PengaduanCreate,
    PengaduanResponse,
    PengaduanUpdate,
)

from app.services.pengaduan_service import (
    PengaduanService,
)

router = APIRouter(
    prefix="/api/pengaduan",
    tags=["Pengaduan"],
)

service = PengaduanService()


@router.get(
    "",
    response_model=list[PengaduanResponse],
)
def list_pengaduan(
    penduduk_id: UUID | None = None,
    rt_id: UUID | None = None,
    status: str | None = None,
    kategori: str | None = None,
    skip: int = Query(
        default=0,
        ge=0,
    ),
    limit: int = Query(
        default=100,
        ge=1,
        le=100,
    ),
    db: Session = Depends(get_db),
):
    return service.list_pengaduan(
        db,
        penduduk_id=penduduk_id,
        rt_id=rt_id,
        status=status,
        kategori=kategori,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/{pengaduan_id}",
    response_model=PengaduanResponse,
)
def get_pengaduan(
    pengaduan_id: UUID,
    db: Session = Depends(get_db),
):
    return service.get_pengaduan(
        db,
        pengaduan_id,
    )


@router.post(
    "",
    response_model=PengaduanResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_pengaduan(
    data: PengaduanCreate,
    db: Session = Depends(get_db),
):
    return service.create_pengaduan(
        db,
        data,
    )


@router.put(
    "/{pengaduan_id}",
    response_model=PengaduanResponse,
)
def update_pengaduan(
    pengaduan_id: UUID,
    data: PengaduanUpdate,
    db: Session = Depends(get_db),
):
    return service.update_pengaduan(
        db,
        pengaduan_id,
        data,
    )
