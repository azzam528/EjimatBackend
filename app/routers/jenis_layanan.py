from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.layanan import (
    JenisLayananCreate,
    JenisLayananResponse,
    JenisLayananUpdate,
)
from app.services.jenis_layanan_service import JenisLayananService

router = APIRouter(prefix="/api/jenis-layanan", tags=["Jenis Layanan"])

service = JenisLayananService()


@router.get("", response_model=list[JenisLayananResponse])
def list_jenis_layanan(
    active_only: bool = Query(default=False), db: Session = Depends(get_db)
):
    return service.list_jenis_layanan(db, active_only=active_only)


@router.get("/{layanan_id}", response_model=JenisLayananResponse)
def get_jenis_layanan(layanan_id: UUID, db: Session = Depends(get_db)):
    return service.get_jenis_layanan(db, layanan_id)


@router.post(
    "", response_model=JenisLayananResponse, status_code=status.HTTP_201_CREATED
)
def create_jenis_layanan(data: JenisLayananCreate, db: Session = Depends(get_db)):
    return service.create_jenis_layanan(db, data)


@router.put("/{layanan_id}", response_model=JenisLayananResponse)
def update_jenis_layanan(
    layanan_id: UUID, data: JenisLayananUpdate, db: Session = Depends(get_db)
):
    return service.update_jenis_layanan(db, layanan_id, data)


@router.delete("/{layanan_id}")
def delete_jenis_layanan(layanan_id: UUID, db: Session = Depends(get_db)):
    service.delete_jenis_layanan(db, layanan_id)

    return {"message": "Jenis layanan deleted successfully"}
