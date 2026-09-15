from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.wilayah import (
    RWCreate,
    RWResponse
)
from app.services.rw_service import RWService


router = APIRouter(
    prefix="/api/rw",
    tags=["RW"]
)

service = RWService()


@router.get(
    "",
    response_model=list[RWResponse]
)
def list_rw(
    db: Session = Depends(get_db)
):
    return service.list_rw(db)


@router.get(
    "/{rw_id}",
    response_model=RWResponse
)
def get_rw(
    rw_id: UUID,
    db: Session = Depends(get_db)
):
    return service.get_rw(
        db,
        rw_id
    )


@router.post(
    "",
    response_model=RWResponse,
    status_code=status.HTTP_201_CREATED
)
def create_rw(
    data: RWCreate,
    db: Session = Depends(get_db)
):
    return service.create_rw(
        db,
        data
    )