from uuid import UUID

from sqlalchemy.orm import Session

from app.models.kependudukan import KartuKeluarga


class KartuKeluargaRepository:

    @staticmethod
    def get_all(db: Session):
        return db.query(KartuKeluarga).all()

    @staticmethod
    def get_by_id(db: Session, kk_id: UUID):
        return (
            db.query(KartuKeluarga)
            .filter(KartuKeluarga.id == kk_id)
            .first()
        )

    @staticmethod
    def get_by_no_kk(db: Session, no_kk: str):
        return (
            db.query(KartuKeluarga)
            .filter(KartuKeluarga.no_kk == no_kk)
            .first()
        )

    @staticmethod
    def create(db: Session, kk: KartuKeluarga):
        db.add(kk)
        db.commit()
        db.refresh(kk)

        return kk

    @staticmethod
    def update(db: Session, kk: KartuKeluarga):
        db.commit()
        db.refresh(kk)

        return kk

    @staticmethod
    def delete(db: Session, kk: KartuKeluarga):
        db.delete(kk)
        db.commit()