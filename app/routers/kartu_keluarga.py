from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.schemas.kependudukan import (
    KartuKeluargaCreate,
    KartuKeluargaUpdate,
    KartuKeluargaResponse
)

from app.services.kartu_keluarga_service import (
    KartuKeluargaService
)


router = APIRouter(
    prefix="/api/kartu-keluarga",
    tags=["Kartu Keluarga"]
)


@router.get(
    "",
    response_model=list[KartuKeluargaResponse]
)
def get_all_kartu_keluarga(
    db: Session = Depends(get_db)
):

    return KartuKeluargaService.get_all(
        db
    )


@router.get(
    "/{kk_id}",
    response_model=KartuKeluargaResponse
)
def get_kartu_keluarga_by_id(
    kk_id: UUID,
    db: Session = Depends(get_db)
):

    return KartuKeluargaService.get_by_id(
        db,
        kk_id
    )


@router.post(
    "",
    response_model=KartuKeluargaResponse,
    status_code=status.HTTP_201_CREATED
)
def create_kartu_keluarga(
    kk_data: KartuKeluargaCreate,
    db: Session = Depends(get_db)
):

    return KartuKeluargaService.create(
        db,
        kk_data
    )


@router.put(
    "/{kk_id}",
    response_model=KartuKeluargaResponse
)
def update_kartu_keluarga(
    kk_id: UUID,
    kk_data: KartuKeluargaUpdate,
    db: Session = Depends(get_db)
):

    return KartuKeluargaService.update(
        db,
        kk_id,
        kk_data
    )


@router.delete(
    "/{kk_id}"
)
def delete_kartu_keluarga(
    kk_id: UUID,
    db: Session = Depends(get_db)
):

    return KartuKeluargaService.delete(
        db,
        kk_id
    )