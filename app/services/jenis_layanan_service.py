from datetime import datetime
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.layanan import JenisLayanan
from app.repositories.jenis_layanan_repository import JenisLayananRepository
from app.schemas.layanan import JenisLayananCreate, JenisLayananUpdate


class JenisLayananService:

    def __init__(self, repository: JenisLayananRepository | None = None):
        self.repository = repository or JenisLayananRepository()

    def list_jenis_layanan(self, db: Session, active_only: bool = False):
        layanan = self.repository.get_all(db)

        if active_only:
            layanan = [item for item in layanan if item.is_active]

        return layanan

    def get_jenis_layanan(self, db: Session, layanan_id: UUID):
        layanan = self.repository.get_by_id(db, layanan_id)

        if layanan is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Jenis layanan not found"
            )

        return layanan

    def create_jenis_layanan(self, db: Session, data: JenisLayananCreate):
        existing = self.repository.get_by_nama(db, data.nama_layanan)

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Jenis layanan already exists",
            )

        jenis_layanan = JenisLayanan(
            **data.model_dump(),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        return self._commit(db, lambda: self.repository.create(db, jenis_layanan))

    def update_jenis_layanan(
        self, db: Session, layanan_id: UUID, data: JenisLayananUpdate
    ):
        jenis_layanan = self.get_jenis_layanan(db, layanan_id)

        update_data = data.model_dump(exclude_unset=True)

        if "nama_layanan" in update_data:
            existing = self.repository.get_by_nama(db, update_data["nama_layanan"])

            if existing and existing.id != layanan_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Jenis layanan already exists",
                )

        for field, value in update_data.items():
            setattr(jenis_layanan, field, value)

        jenis_layanan.updated_at = datetime.utcnow()

        return self._commit(db, lambda: self.repository.update(db, jenis_layanan))

    def delete_jenis_layanan(self, db: Session, layanan_id: UUID):
        jenis_layanan = self.get_jenis_layanan(db, layanan_id)

        # Untuk sementara hard delete.
        # Nanti bisa kita ubah menjadi soft delete
        # jika sudah ada pengajuan layanan yang memakai data ini.

        return self._commit(db, lambda: self.repository.delete(db, jenis_layanan))

    @staticmethod
    def _commit(db: Session, operation):
        try:
            return operation()

        except SQLAlchemyError:
            db.rollback()

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Database operation failed",
            )
