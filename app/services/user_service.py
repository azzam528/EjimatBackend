from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.core.security import hash_password
from app.models.users import User, Role
from app.schemas.users import UserCreate


class UserService:
    def list_users(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 20,
    ):
        return (
            db.query(User)
            .options(joinedload(User.role))
            .order_by(User.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_user(self, db: Session, user_id: UUID) -> User:
        user = (
            db.query(User)
            .options(joinedload(User.role))
            .filter(User.id == user_id)
            .first()
        )

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        return user

    def create_user(
        self,
        db: Session,
        payload: UserCreate,
    ) -> User:
        existing_user = db.query(User).filter(User.username == payload.username).first()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username already exists",
            )

        if payload.email:
            existing_email = db.query(User).filter(User.email == payload.email).first()

            if existing_email:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email already exists",
                )

        role = db.query(Role).filter(Role.id == payload.role_id).first()

        if role is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Role not found",
            )

        user_data = payload.model_dump(exclude={"password"})
        user = User(
            **user_data,
            password_hash=hash_password(payload.password),
            is_active=True,
        )

        db.add(user)

        try:
            db.commit()
            db.refresh(user)
        except Exception:
            db.rollback()
            raise

        return self.get_user(db, user.id)

    def set_user_active(
        self,
        db: Session,
        user_id: UUID,
        is_active: bool,
    ) -> User:
        user = self.get_user(db, user_id)
        user.is_active = is_active

        try:
            db.commit()
            db.refresh(user)
        except Exception:
            db.rollback()
            raise

        return self.get_user(db, user_id)


user_service = UserService()
