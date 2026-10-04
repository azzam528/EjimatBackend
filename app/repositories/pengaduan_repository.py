from uuid import UUID

from sqlalchemy.orm import Session

from app.models.pengaduan import Pengaduan


class PengaduanRepository:

    def get_all(
        self,
        db: Session,
        penduduk_id: UUID | None = None,
        status: str | None = None,
        skip: int = 0,
        limit: int = 100,
    ):
        query = db.query(Pengaduan)

        if penduduk_id is not None:
            query = query.filter(Pengaduan.penduduk_id == penduduk_id)

        if status is not None:
            query = query.filter(Pengaduan.status == status)

        return (
            query.order_by(Pengaduan.created_at.desc()).offset(skip).limit(limit).all()
        )

    def get_by_id(
        self,
        db: Session,
        pengaduan_id: UUID,
    ):
        return db.query(Pengaduan).filter(Pengaduan.id == pengaduan_id).first()

    def create(
        self,
        db: Session,
        pengaduan: Pengaduan,
    ):
        db.add(pengaduan)
        db.commit()
        db.refresh(pengaduan)

        return pengaduan

    def update(
        self,
        db: Session,
        pengaduan: Pengaduan,
    ):
        db.commit()
        db.refresh(pengaduan)

        return pengaduan
