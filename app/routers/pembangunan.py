from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.pembangunan import (
    PembangunanCreate,
    PembangunanResponse,
    PembangunanUpdate,
)
from app.services.pembangunan_service import PembangunanService

router = APIRouter(
    prefix="/api/pembangunan",
    tags=["Pembangunan"],
)

service = PembangunanService()


@router.get("", response_model=list[PembangunanResponse])
def list_pembangunan(
    rt_id: UUID | None = None,
    status_filter: str | None = Query(
        default=None,
        alias="status",
    ),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return service.list_pembangunan(
        db,
        rt_id=rt_id,
        status_filter=status_filter,
        skip=skip,
        limit=limit,
    )


@router.get("/{pembangunan_id}", response_model=PembangunanResponse)
def get_pembangunan(
    pembangunan_id: UUID,
    db: Session = Depends(get_db),
):
    return service.get_pembangunan(
        db,
        pembangunan_id,
    )


@router.post(
    "",
    response_model=PembangunanResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_pembangunan(
    data: PembangunanCreate,
    db: Session = Depends(get_db),
):
    return service.create_pembangunan(db, data)


@router.put(
    "/{pembangunan_id}",
    response_model=PembangunanResponse,
)
def update_pembangunan(
    pembangunan_id: UUID,
    data: PembangunanUpdate,
    db: Session = Depends(get_db),
):
    return service.update_pembangunan(
        db,
        pembangunan_id,
        data,
    )


@router.delete("/{pembangunan_id}")
def delete_pembangunan(
    pembangunan_id: UUID,
    db: Session = Depends(get_db),
):
    return service.delete_pembangunan(
        db,
        pembangunan_id,
    )
