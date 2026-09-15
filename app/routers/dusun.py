from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.wilayah import (
    DusunCreate,
    DusunResponse
)
from app.services.dusun_service import DusunService


router = APIRouter(
    prefix="/api/dusun",
    tags=["Dusun"]
)

service = DusunService()


@router.get(
    "",
    response_model=list[DusunResponse]
)
def list_dusun(
    db: Session = Depends(get_db)
):
    return service.list_dusun(db)


@router.get(
    "/{dusun_id}",
    response_model=DusunResponse
)
def get_dusun(
    dusun_id: UUID,
    db: Session = Depends(get_db)
):
    return service.get_dusun(
        db,
        dusun_id
    )


@router.post(
    "",
    response_model=DusunResponse,
    status_code=status.HTTP_201_CREATED
)
def create_dusun(
    data: DusunCreate,
    db: Session = Depends(get_db)
):
    return service.create_dusun(
        db,
        data
    )