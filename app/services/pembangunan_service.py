import uuid
from datetime import date, datetime
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.pembangunan import Pembangunan
from app.models.wilayah import RT
from app.repositories.pembangunan_repository import PembangunanRepository
from app.schemas.pembangunan import PembangunanCreate, PembangunanUpdate

ALLOWED_STATUS = {
    "direncanakan",
    "berjalan",
    "selesai",
    "ditunda",
    "dibatalkan",
}


class PembangunanService:

    def __init__(
        self,
        repository: PembangunanRepository | None = None,
    ):
        self.repository = repository or PembangunanRepository()

    def list_pembangunan(
        self,
        db: Session,
        rt_id: UUID | None = None,
        status_filter: str | None = None,
        skip: int = 0,
        limit: int = 100,
    ):
        if status_filter is not None:
            self._validate_status(status_filter)

        return self.repository.get_all(
            db,
            rt_id=rt_id,
            status=status_filter,
            skip=skip,
            limit=limit,
        )

    def get_pembangunan(
        self,
        db: Session,
        pembangunan_id: UUID,
    ):
        item = self.repository.get_by_id(db, pembangunan_id)

        if item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Data pembangunan tidak ditemukan",
            )

        return item

    def create_pembangunan(
        self,
        db: Session,
        data: PembangunanCreate,
    ):
        payload = data.model_dump()

        self._validate_status(payload["status"])
        self._validate_dates(
            payload.get("tanggal_mulai"),
            payload.get("target_selesai"),
            payload.get("tanggal_selesai"),
        )

        if payload.get("rt_id") is not None:
            self._validate_rt(db, payload["rt_id"])

        now = datetime.utcnow()

        item = Pembangunan(
            id=uuid.uuid4(),
            **payload,
            created_at=now,
            updated_at=now,
        )

        try:
            return self.repository.create(db, item)
        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Gagal menyimpan data pembangunan",
            )

    def update_pembangunan(
        self,
        db: Session,
        pembangunan_id: UUID,
        data: PembangunanUpdate,
    ):
        item = self.get_pembangunan(db, pembangunan_id)
        payload = data.model_dump(exclude_unset=True)

        if "status" in payload and payload["status"] is not None:
            self._validate_status(payload["status"])

        if "rt_id" in payload and payload["rt_id"] is not None:
            self._validate_rt(db, payload["rt_id"])

        tanggal_mulai = payload.get(
            "tanggal_mulai",
            item.tanggal_mulai,
        )
        target_selesai = payload.get(
            "target_selesai",
            item.target_selesai,
        )
        tanggal_selesai = payload.get(
            "tanggal_selesai",
            item.tanggal_selesai,
        )

        self._validate_dates(
            tanggal_mulai,
            target_selesai,
            tanggal_selesai,
        )

        for field, value in payload.items():
            setattr(item, field, value)

        item.updated_at = datetime.utcnow()

        try:
            return self.repository.update(db, item)
        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Gagal memperbarui data pembangunan",
            )

    def delete_pembangunan(
        self,
        db: Session,
        pembangunan_id: UUID,
    ):
        item = self.get_pembangunan(db, pembangunan_id)

        try:
            self.repository.delete(db, item)
        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    "Data pembangunan tidak dapat dihapus. "
                    "Periksa apakah masih memiliki dokumentasi."
                ),
            )

        return {"message": "Data pembangunan berhasil dihapus"}

    @staticmethod
    def _validate_status(value: str):
        if value not in ALLOWED_STATUS:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={
                    "message": "Status pembangunan tidak valid",
                    "allowed_status": sorted(ALLOWED_STATUS),
                },
            )

    @staticmethod
    def _validate_rt(db: Session, rt_id: UUID):
        rt = db.query(RT).filter(RT.id == rt_id).first()

        if rt is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Data RT tidak ditemukan",
            )

    @staticmethod
    def _validate_dates(
        tanggal_mulai: date | None,
        target_selesai: date | None,
        tanggal_selesai: date | None,
    ):
        if (
            tanggal_mulai is not None
            and target_selesai is not None
            and target_selesai < tanggal_mulai
        ):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Target selesai tidak boleh sebelum tanggal mulai",
            )

        if (
            tanggal_selesai is not None
            and tanggal_mulai is not None
            and tanggal_selesai < tanggal_mulai
        ):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Tanggal selesai tidak boleh sebelum tanggal mulai",
            )
