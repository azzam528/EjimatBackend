from datetime import datetime
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.kependudukan import Penduduk
from app.repositories.penduduk_repository import PendudukRepository
from app.schemas.kependudukan import PendudukCreate, PendudukUpdate
from app.services.duplicate_detection_service import (
    DuplicateDetectionService
)

class PendudukService:
    def __init__(self, repository: PendudukRepository | None = None):
        self.repository = repository or PendudukRepository()

    def list_penduduk(self, db: Session, **filters) -> list[Penduduk]:
        return self.repository.get_all(db, **filters)

    def get_penduduk(self, db: Session, penduduk_id: UUID) -> Penduduk:
        penduduk = self.repository.get_by_id(db, penduduk_id)
        if penduduk is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Penduduk not found")
        return penduduk

    def create_penduduk(
        self,
        db: Session,
        data: PendudukCreate,
        force_save: bool = False
    ) -> Penduduk:

        # =========================
        # 1. CEK NIK DUPLIKAT
        # =========================

        existing_nik = (
            self.repository.get_by_nik(
                db,
                data.nik
            )
        )

        if existing_nik:

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "type": "exact_duplicate",
                    "message":
                        "NIK sudah terdaftar",
                    "existing_penduduk": {
                        "id": str(existing_nik.id),
                        "nik": existing_nik.nik,
                        "nama_lengkap":
                            existing_nik.nama_lengkap
                    }
                }
            )


        # =========================
        # 2. DUPLICATE DETECTION
        # =========================

        possible_duplicates = (
            DuplicateDetectionService.check_penduduk(
                db=db,
                repository=self.repository,
                data=data
            )
        )


        # =========================
        # 3. WARNING DUPLIKAT
        # =========================

        if (
            possible_duplicates
            and not force_save
        ):

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "type":
                        "possible_duplicate",

                    "message":
                        "Ditemukan kemungkinan data duplikat. "
                        "Gunakan force_save=true jika ingin "
                        "tetap menyimpan.",

                    "possible_duplicates":
                        possible_duplicates
                }
            )


        # =========================
        # 4. SIMPAN DATA
        # =========================

        penduduk = Penduduk(
            **data.model_dump(),
            created_at=datetime.utcnow()
        )

        return self._commit(
            db,
            lambda:
            self.repository.create(
                db,
                penduduk
            )
        )

    def update_penduduk(self, db: Session, penduduk_id: UUID, data: PendudukUpdate) -> Penduduk:
        penduduk = self.get_penduduk(db, penduduk_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(penduduk, field, value)
        penduduk.updated_at = datetime.utcnow()
        return self._commit(db, lambda: self.repository.update(db, penduduk))

    def delete_penduduk(self, db: Session, penduduk_id: UUID) -> None:
        penduduk = self.get_penduduk(db, penduduk_id)
        self._commit(db, lambda: self.repository.delete(db, penduduk))

    @staticmethod
    def _commit(db: Session, operation):
        try:
            return operation()
        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Database operation failed")
