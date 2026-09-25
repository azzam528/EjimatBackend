from uuid import UUID

from sqlalchemy.orm import Session

from app.models.layanan import DokumenPengajuan


class DokumenPengajuanRepository:

    def get_all_by_pengajuan(
        self,
        db: Session,
        pengajuan_id: UUID,
    ):
        return (
            db.query(DokumenPengajuan)
            .filter(DokumenPengajuan.pengajuan_id == pengajuan_id)
            .order_by(DokumenPengajuan.uploaded_at.desc())
            .all()
        )

    def get_by_id(
        self,
        db: Session,
        dokumen_id: UUID,
    ):
        return (
            db.query(DokumenPengajuan)
            .filter(DokumenPengajuan.id == dokumen_id)
            .first()
        )

    def create(
        self,
        db: Session,
        dokumen: DokumenPengajuan,
    ):
        db.add(dokumen)
        db.commit()
        db.refresh(dokumen)

        return dokumen

    def delete(
        self,
        db: Session,
        dokumen: DokumenPengajuan,
    ):
        db.delete(dokumen)
        db.commit()