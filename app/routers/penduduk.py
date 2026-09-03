from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.kependudukan import PendudukCreate, PendudukResponse, PendudukUpdate
from app.services.penduduk_service import PendudukService

router = APIRouter()
service = PendudukService()


@router.get("", response_model=list[PendudukResponse])
def list_penduduk(
    search: str | None = None,
    rt_id: UUID | None = None,
    status_penduduk: str | None = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return service.list_penduduk(
        db,
        search=search,
        rt_id=rt_id,
        status_penduduk=status_penduduk,
        skip=skip,
        limit=limit,
    )


@router.get("/{penduduk_id}", response_model=PendudukResponse)
def get_penduduk(penduduk_id: UUID, db: Session = Depends(get_db)):
    return service.get_penduduk(db, penduduk_id)


@router.post("", response_model=PendudukResponse, status_code=status.HTTP_201_CREATED)
def create_penduduk(data: PendudukCreate, db: Session = Depends(get_db)):
    return service.create_penduduk(db, data)


@router.put("/{penduduk_id}", response_model=PendudukResponse)
def update_penduduk(penduduk_id: UUID, data: PendudukUpdate, db: Session = Depends(get_db)):
    return service.update_penduduk(db, penduduk_id, data)


@router.delete("/{penduduk_id}")
def delete_penduduk(penduduk_id: UUID, db: Session = Depends(get_db)):
    service.delete_penduduk(db, penduduk_id)
    return {"message": "Penduduk deleted successfully"}
