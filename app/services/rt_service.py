import uuid

from datetime import datetime

from uuid import UUID

from fastapi import HTTPException, status

from sqlalchemy.exc import SQLAlchemyError

from sqlalchemy.orm import Session

from app.models.wilayah import RT, RW

from app.repositories.rt_repository import RTRepository

from app.schemas.wilayah import RTCreate


class RTService:

    def __init__(
        self,
        repository: RTRepository | None = None
    ):
        self.repository = (
            repository or RTRepository()
        )

    def list_rt(
        self,
        db: Session
    ) -> list[RT]:

        return self.repository.get_all(db)

    def get_rt(
        self,
        db: Session,
        rt_id: UUID
    ) -> RT:

        rt = self.repository.get_by_id(
            db,
            rt_id
        )

        if rt is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="RT not found"
            )

        return rt

    def create_rt(
        self,
        db: Session,
        data: RTCreate
    ) -> RT:

        # =========================
        # CEK RW
        # =========================

        rw = (
            db.query(RW)
            .filter(RW.id == data.rw_id)
            .first()
        )

        if rw is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="RW not found"
            )

        # =========================
        # CEK CODE
        # =========================

        if data.code:

            existing = (
                self.repository.get_by_code(
                    db,
                    data.code
                )
            )

            if existing:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="RT code already exists"
                )

        # =========================
        # CREATE
        # =========================

        rt = RT(
            id=uuid.uuid4(),
            rw_id=data.rw_id,
            number=data.number,
            code=data.code,
            created_at=datetime.utcnow()
        )

        return self._commit(
            db,
            lambda: self.repository.create(
                db,
                rt
            )
        )

    @staticmethod
    def _commit(
        db: Session,
        operation
    ):

        try:

            return operation()

        except SQLAlchemyError:

            db.rollback()

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Database operation failed"
            )