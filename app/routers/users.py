from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.permissions import require_roles
from app.database.database import get_db
from app.models.users import User
from app.schemas.users import UserCreate, UserResponse
from app.services.user_service import user_service

router = APIRouter(
    prefix="/api/users",
    tags=["User Management"],
)


@router.get(
    "",
    response_model=list[UserResponse],
)
def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("Admin")),
):
    return user_service.list_users(db, skip, limit)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
)
def get_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("Admin")),
):
    return user_service.get_user(db, user_id)


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("Admin")),
):
    return user_service.create_user(db, payload)


@router.patch(
    "/{user_id}/status",
    response_model=UserResponse,
)
def update_user_status(
    user_id: UUID,
    is_active: bool,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("Admin")),
):
    return user_service.set_user_active(db, user_id, is_active)
