from uuid import UUID

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.kependudukan import Penduduk


class PendudukRepository:
    def get_all(
        self,
        db: Session,
        *,
        search: str | None = None,
        rt_id: UUID | None = None,
        status_penduduk: str | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Penduduk]:
        query = db.query(Penduduk)

        if search:
            keyword = f"%{search}%"
            query = query.filter(
                or_(Penduduk.nik.ilike(keyword), Penduduk.nama_lengkap.ilike(keyword))
            )
        if rt_id is not None:
            query = query.filter(Penduduk.rt_id == rt_id)
        if status_penduduk is not None:
            query = query.filter(Penduduk.status_penduduk == status_penduduk)

        return query.offset(skip).limit(limit).all()

    def get_by_id(self, db: Session, penduduk_id: UUID) -> Penduduk | None:
        return db.query(Penduduk).filter(Penduduk.id == penduduk_id).first()

    def create(self, db: Session, penduduk: Penduduk) -> Penduduk:
        db.add(penduduk)
        db.commit()
        db.refresh(penduduk)
        return penduduk

    def update(self, db: Session, penduduk: Penduduk) -> Penduduk:
        db.commit()
        db.refresh(penduduk)
        return penduduk

    def delete(self, db: Session, penduduk: Penduduk) -> None:
        db.delete(penduduk)
        db.commit()
