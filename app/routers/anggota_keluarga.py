from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.schemas.kependudukan import AnggotaKeluargaCreate, AnggotaKeluargaResponse

from app.services.anggota_keluarga_service import AnggotaKeluargaService

router = APIRouter(prefix="/api/anggota-keluarga", tags=["Anggota Keluarga"])

service = AnggotaKeluargaService()


@router.get("", response_model=list[AnggotaKeluargaResponse])
def list_anggota_keluarga(
    kk_id: UUID | None = None,
    penduduk_id: UUID | None = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return service.list_anggota_keluarga(
        db, kk_id=kk_id, penduduk_id=penduduk_id, skip=skip, limit=limit
    )


@router.get("/{anggota_id}", response_model=AnggotaKeluargaResponse)
def get_anggota_keluarga(anggota_id: UUID, db: Session = Depends(get_db)):
    return service.get_anggota_keluarga(db, anggota_id)


@router.post(
    "", response_model=AnggotaKeluargaResponse, status_code=status.HTTP_201_CREATED
)
def create_anggota_keluarga(data: AnggotaKeluargaCreate, db: Session = Depends(get_db)):
    return service.create_anggota_keluarga(db, data)


@router.delete("/{anggota_id}")
def delete_anggota_keluarga(anggota_id: UUID, db: Session = Depends(get_db)):
    service.delete_anggota_keluarga(db, anggota_id)

    return {"message": "Anggota keluarga deleted successfully"}
