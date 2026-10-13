from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.informasi import (
    BeritaCreate,
    BeritaResponse,
    BeritaUpdate,
    PengumumanCreate,
    PengumumanResponse,
    PengumumanUpdate,
)
from app.services.informasi_service import InformasiService

berita_router = APIRouter(prefix="/api/berita", tags=["Berita"])
pengumuman_router = APIRouter(prefix="/api/pengumuman", tags=["Pengumuman"])

service = InformasiService()


@berita_router.get("", response_model=list[BeritaResponse])
def list_berita(
    status_filter: str = Query(default="published", alias="status"),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return service.list_items(db, "berita", status_filter, skip, limit)


@berita_router.get("/{item_id}", response_model=BeritaResponse)
def get_berita(item_id: UUID, db: Session = Depends(get_db)):
    return service.get_item(db, "berita", item_id)


@berita_router.post(
    "",
    response_model=BeritaResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_berita(data: BeritaCreate, db: Session = Depends(get_db)):
    return service.create_item(db, "berita", data)


@berita_router.put("/{item_id}", response_model=BeritaResponse)
def update_berita(
    item_id: UUID,
    data: BeritaUpdate,
    db: Session = Depends(get_db),
):
    return service.update_item(db, "berita", item_id, data)


@berita_router.delete("/{item_id}")
def delete_berita(item_id: UUID, db: Session = Depends(get_db)):
    return service.delete_item(db, "berita", item_id)


@pengumuman_router.get("", response_model=list[PengumumanResponse])
def list_pengumuman(
    status_filter: str = Query(default="published", alias="status"),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return service.list_items(db, "pengumuman", status_filter, skip, limit)


@pengumuman_router.get("/{item_id}", response_model=PengumumanResponse)
def get_pengumuman(item_id: UUID, db: Session = Depends(get_db)):
    return service.get_item(db, "pengumuman", item_id)


@pengumuman_router.post(
    "",
    response_model=PengumumanResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_pengumuman(data: PengumumanCreate, db: Session = Depends(get_db)):
    return service.create_item(db, "pengumuman", data)


@pengumuman_router.put("/{item_id}", response_model=PengumumanResponse)
def update_pengumuman(
    item_id: UUID,
    data: PengumumanUpdate,
    db: Session = Depends(get_db),
):
    return service.update_item(db, "pengumuman", item_id, data)


@pengumuman_router.delete("/{item_id}")
def delete_pengumuman(item_id: UUID, db: Session = Depends(get_db)):
    return service.delete_item(db, "pengumuman", item_id)
