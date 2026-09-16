from uuid import UUID

from sqlalchemy.orm import Session

from app.models.wilayah import RT


class RTRepository:

    def get_all(self, db: Session) -> list[RT]:
        return db.query(RT).all()

    def get_by_id(
        self,
        db: Session,
        rt_id: UUID
    ) -> RT | None:
        return (
            db.query(RT)
            .filter(RT.id == rt_id)
            .first()
        )

    def get_by_code(
        self,
        db: Session,
        code: str
    ) -> RT | None:
        return (
            db.query(RT)
            .filter(RT.code == code)
            .first()
        )

    def create(
        self,
        db: Session,
        rt: RT
    ) -> RT:
        db.add(rt)
        db.commit()
        db.refresh(rt)
        return rt

    def update(
        self,
        db: Session,
        rt: RT
    ) -> RT:
        db.commit()
        db.refresh(rt)
        return rt

    def delete(
        self,
        db: Session,
        rt: RT
    ) -> None:
        db.delete(rt)
        db.commit()