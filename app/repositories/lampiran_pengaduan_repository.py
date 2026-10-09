
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.pengaduan import LampiranPengaduan


class LampiranPengaduanRepository:

    def get_all_by_pengaduan(
        self,
        db: Session,
        pengaduan_id: UUID,
    ):
        return (
            db.query(LampiranPengaduan)
            .filter(LampiranPengaduan.pengaduan_id == pengaduan_id)
            .order_by(LampiranPengaduan.created_at.desc())
            .all()
        )

    def get_by_id(
        self,
        db: Session,
        lampiran_id: UUID,
    ):
        return (
            db.query(LampiranPengaduan)
            .filter(LampiranPengaduan.id == lampiran_id)
            .first()
        )

    def create(
        self,
        db: Session,
        lampiran: LampiranPengaduan,
    ):
        db.add(lampiran)
        db.commit()
        db.refresh(lampiran)
        return lampiran

    def delete(
        self,
        db: Session,
        lampiran: LampiranPengaduan,
    ):
        db.delete(lampiran)
        db.commit()