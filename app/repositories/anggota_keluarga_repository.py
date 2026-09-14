from uuid import UUID

from sqlalchemy.orm import Session

from app.models.kependudukan import AnggotaKeluarga


class AnggotaKeluargaRepository:

    @staticmethod
    def get_all(db: Session):
        return db.query(AnggotaKeluarga).all()

    @staticmethod
    def get_by_id(
        db: Session,
        anggota_id: UUID
    ):
        return (
            db.query(AnggotaKeluarga)
            .filter(
                AnggotaKeluarga.id == anggota_id
            )
            .first()
        )

    @staticmethod
    def get_by_kk_id(
        db: Session,
        kk_id: UUID
    ):
        return (
            db.query(AnggotaKeluarga)
            .filter(
                AnggotaKeluarga.kk_id == kk_id
            )
            .all()
        )

    @staticmethod
    def get_by_penduduk_id(
        db: Session,
        penduduk_id: UUID
    ):
        return (
            db.query(AnggotaKeluarga)
            .filter(
                AnggotaKeluarga.penduduk_id == penduduk_id
            )
            .first()
        )

    @staticmethod
    def create(
        db: Session,
        anggota: AnggotaKeluarga
    ):
        db.add(anggota)
        db.commit()
        db.refresh(anggota)

        return anggota

    @staticmethod
    def update(
        db: Session,
        anggota: AnggotaKeluarga
    ):
        db.commit()
        db.refresh(anggota)

        return anggota

    @staticmethod
    def delete(
        db: Session,
        anggota: AnggotaKeluarga
    ):
        db.delete(anggota)
        db.commit()