from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.schemas.kependudukan import (
    AnggotaKeluargaCreate,
    AnggotaKeluargaUpdate,
    AnggotaKeluargaResponse
)

from app.services.anggota_keluarga_service import (
    AnggotaKeluargaService
)


router = APIRouter(
    prefix="/api/anggota-keluarga",
    tags=["Anggota Keluarga"]
)


# =========================
# GET ALL
# =========================

@router.get(
    "",
    response_model=list[AnggotaKeluargaResponse]
)
def get_all_anggota_keluarga(
    db: Session = Depends(get_db)
):

    return AnggotaKeluargaService.get_all(db)


# =========================
# GET BY ID
# =========================

@router.get(
    "/{anggota_id}",
    response_model=AnggotaKeluargaResponse
)
def get_anggota_keluarga_by_id(
    anggota_id: UUID,
    db: Session = Depends(get_db)
):

    return (
        AnggotaKeluargaService.get_by_id(
            db,
            anggota_id
        )
    )


# =========================
# GET BY KK
# =========================

@router.get(
    "/kk/{kk_id}",
    response_model=list[AnggotaKeluargaResponse]
)
def get_anggota_by_kk(
    kk_id: UUID,
    db: Session = Depends(get_db)
):

    return (
        AnggotaKeluargaService.get_by_kk_id(
            db,
            kk_id
        )
    )


# =========================
# CREATE
# =========================

@router.post(
    "",
    response_model=AnggotaKeluargaResponse,
    status_code=status.HTTP_201_CREATED
)
def create_anggota_keluarga(
    anggota_data: AnggotaKeluargaCreate,
    db: Session = Depends(get_db)
):

    return (
        AnggotaKeluargaService.create(
            db,
            anggota_data
        )
    )


# =========================
# UPDATE
# =========================

@router.put(
    "/{anggota_id}",
    response_model=AnggotaKeluargaResponse
)
def update_anggota_keluarga(
    anggota_id: UUID,
    anggota_data: AnggotaKeluargaUpdate,
    db: Session = Depends(get_db)
):

    return (
        AnggotaKeluargaService.update(
            db,
            anggota_id,
            anggota_data
        )
    )


# =========================
# DELETE
# =========================

@router.delete(
    "/{anggota_id}"
)
def delete_anggota_keluarga(
    anggota_id: UUID,
    db: Session = Depends(get_db)
):

    return (
        AnggotaKeluargaService.delete(
            db,
            anggota_id
        )
    )