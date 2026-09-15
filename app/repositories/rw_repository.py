from uuid import UUID

from sqlalchemy.orm import Session

from app.models.wilayah import RW


class RWRepository:

    def get_all(self, db: Session) -> list[RW]:
        return db.query(RW).all()

    def get_by_id(
        self,
        db: Session,
        rw_id: UUID
    ) -> RW | None:
        return (
            db.query(RW)
            .filter(RW.id == rw_id)
            .first()
        )

    def get_by_code(
        self,
        db: Session,
        code: str
    ) -> RW | None:
        return (
            db.query(RW)
            .filter(RW.code == code)
            .first()
        )

    def create(
        self,
        db: Session,
        rw: RW
    ) -> RW:
        db.add(rw)
        db.commit()
        db.refresh(rw)
        return rw

    def update(
        self,
        db: Session,
        rw: RW
    ) -> RW:
        db.commit()
        db.refresh(rw)
        return rw

    def delete(
        self,
        db: Session,
        rw: RW
    ) -> None:
        db.delete(rw)
        db.commit()