import uuid
from datetime import datetime
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.wilayah import RW
from app.repositories.rw_repository import RWRepository
from app.schemas.wilayah import RWCreate


class RWService:

    def __init__(
        self,
        repository: RWRepository | None = None
    ):
        self.repository = repository or RWRepository()

    def list_rw(
        self,
        db: Session
    ) -> list[RW]:
        return self.repository.get_all(db)

    def get_rw(
        self,
        db: Session,
        rw_id: UUID
    ) -> RW:

        rw = self.repository.get_by_id(
            db,
            rw_id
        )

        if rw is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="RW not found"
            )

        return rw

    def create_rw(
        self,
        db: Session,
        data: RWCreate
    ) -> RW:

        # Pastikan Dusun yang dipilih ada
        from app.models.wilayah import Dusun

        dusun = (
            db.query(Dusun)
            .filter(Dusun.id == data.dusun_id)
            .first()
        )

        if dusun is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Dusun not found"
            )

        # Cek code RW
        if data.code:
            existing = self.repository.get_by_code(
                db,
                data.code
            )

            if existing:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="RW code already exists"
                )

        rw = RW(
            id=uuid.uuid4(),
            dusun_id=data.dusun_id,
            number=data.number,
            code=data.code,
            created_at=datetime.utcnow()
        )

        return self._commit(
            db,
            lambda: self.repository.create(
                db,
                rw
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