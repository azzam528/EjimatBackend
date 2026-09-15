import uuid
from datetime import datetime
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.wilayah import Dusun
from app.repositories.dusun_repository import DusunRepository
from app.schemas.wilayah import DusunCreate


class DusunService:

    def __init__(
        self,
        repository: DusunRepository | None = None
    ):
        self.repository = repository or DusunRepository()

    def list_dusun(
        self,
        db: Session
    ) -> list[Dusun]:
        return self.repository.get_all(db)

    def get_dusun(
        self,
        db: Session,
        dusun_id: UUID
    ) -> Dusun:

        dusun = self.repository.get_by_id(
            db,
            dusun_id
        )

        if dusun is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Dusun not found"
            )

        return dusun

    def create_dusun(
        self,
        db: Session,
        data: DusunCreate
    ) -> Dusun:

        if data.code:
            existing = self.repository.get_by_code(
                db,
                data.code
            )

            if existing:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Dusun code already exists"
                )

        dusun = Dusun(
            id=uuid.uuid4(),
            name=data.name,
            code=data.code,
            created_at=datetime.utcnow()
        )

        return self._commit(
            db,
            lambda: self.repository.create(
                db,
                dusun
            )
        )

    @staticmethod
    def _commit(db: Session, operation):
        try:
            return operation()

        except SQLAlchemyError:
            db.rollback()

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Database operation failed"
            )