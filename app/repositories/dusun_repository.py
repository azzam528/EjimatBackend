from uuid import UUID

from sqlalchemy.orm import Session

from app.models.wilayah import Dusun


class DusunRepository:

    def get_all(self, db: Session) -> list[Dusun]:
        return db.query(Dusun).all()

    def get_by_id(
        self,
        db: Session,
        dusun_id: UUID
    ) -> Dusun | None:
        return (
            db.query(Dusun)
            .filter(Dusun.id == dusun_id)
            .first()
        )

    def get_by_code(
        self,
        db: Session,
        code: str
    ) -> Dusun | None:
        return (
            db.query(Dusun)
            .filter(Dusun.code == code)
            .first()
        )

    def create(
        self,
        db: Session,
        dusun: Dusun
    ) -> Dusun:
        db.add(dusun)
        db.commit()
        db.refresh(dusun)
        return dusun

    def update(
        self,
        db: Session,
        dusun: Dusun
    ) -> Dusun:
        db.commit()
        db.refresh(dusun)
        return dusun

    def delete(
        self,
        db: Session,
        dusun: Dusun
    ) -> None:
        db.delete(dusun)
        db.commit()