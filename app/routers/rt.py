from uuid import UUID

from fastapi import APIRouter, Depends, status

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.schemas.wilayah import (
    RTCreate,
    RTResponse
)

from app.services.rt_service import RTService


router = APIRouter(
    prefix="/api/rt",
    tags=["RT"]
)

service = RTService()


@router.get(
    "",
    response_model=list[RTResponse]
)
def list_rt(
    db: Session = Depends(get_db)
):

    return service.list_rt(db)


@router.get(
    "/{rt_id}",
    response_model=RTResponse
)
def get_rt(
    rt_id: UUID,
    db: Session = Depends(get_db)
):

    return service.get_rt(
        db,
        rt_id
    )


@router.post(
    "",
    response_model=RTResponse,
    status_code=status.HTTP_201_CREATED
)
def create_rt(
    data: RTCreate,
    db: Session = Depends(get_db)
):

    return service.create_rt(
        db,
        data
    )