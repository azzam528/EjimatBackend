from uuid import UUID

from sqlalchemy.orm import Session

from app.models.pembangunan import DokumentasiPembangunan


class DokumentasiPembangunanRepository:

    def get_all_by_pembangunan(
        self,
        db: Session,
        pembangunan_id: UUID,
    ):
        return (
            db.query(DokumentasiPembangunan)
            .filter(
                DokumentasiPembangunan.pembangunan_id == pembangunan_id
            )
            .order_by(
                DokumentasiPembangunan.uploaded_at.desc()
            )
            .all()
        )

    def get_by_id(
        self,
        db: Session,
        dokumentasi_id: UUID,
    ):
        return (
            db.query(DokumentasiPembangunan)
            .filter(DokumentasiPembangunan.id == dokumentasi_id)
            .first()
        )

    def create(
        self,
        db: Session,
        dokumentasi: DokumentasiPembangunan,
    ):
        try:
            db.add(dokumentasi)
            db.commit()
            db.refresh(dokumentasi)
            return dokumentasi
        except Exception:
            db.rollback()
            raise

    def delete(
        self,
        db: Session,
        dokumentasi: DokumentasiPembangunan,
    ):
        try:
            db.delete(dokumentasi)
            db.commit()
        except Exception:
            db.rollback()
            raise