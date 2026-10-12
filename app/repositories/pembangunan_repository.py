from uuid import UUID

from sqlalchemy.orm import Session

from app.models.pembangunan import Pembangunan


class PembangunanRepository:

    def get_all(
        self,
        db: Session,
        *,
        rt_id: UUID | None = None,
        status: str | None = None,
        skip: int = 0,
        limit: int = 100,
    ):
        query = db.query(Pembangunan)

        if rt_id is not None:
            query = query.filter(Pembangunan.rt_id == rt_id)

        if status is not None:
            query = query.filter(Pembangunan.status == status)

        return (
            query.order_by(Pembangunan.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_id(self, db: Session, pembangunan_id: UUID):
        return db.query(Pembangunan).filter(Pembangunan.id == pembangunan_id).first()

    def create(self, db: Session, pembangunan: Pembangunan):
        try:
            db.add(pembangunan)
            db.commit()
            db.refresh(pembangunan)
            return pembangunan
        except Exception:
            db.rollback()
            raise

    def update(self, db: Session, pembangunan: Pembangunan):
        try:
            db.commit()
            db.refresh(pembangunan)
            return pembangunan
        except Exception:
            db.rollback()
            raise

    def delete(self, db: Session, pembangunan: Pembangunan):
        try:
            db.delete(pembangunan)
            db.commit()
        except Exception:
            db.rollback()
            raise
