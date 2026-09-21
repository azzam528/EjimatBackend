from uuid import UUID

from sqlalchemy.orm import Session

from app.models.kependudukan import AnggotaKeluarga


class AnggotaKeluargaRepository:

    def get_all(
        self,
        db: Session,
        kk_id: UUID | None = None,
        penduduk_id: UUID | None = None,
        skip: int = 0,
        limit: int = 100,
    ):
        query = db.query(AnggotaKeluarga)

        if kk_id is not None:
            query = query.filter(AnggotaKeluarga.kk_id == kk_id)

        if penduduk_id is not None:
            query = query.filter(AnggotaKeluarga.penduduk_id == penduduk_id)

        return query.offset(skip).limit(limit).all()

    def get_by_id(self, db: Session, anggota_id: UUID):
        return (
            db.query(AnggotaKeluarga).filter(AnggotaKeluarga.id == anggota_id).first()
        )

    def get_by_kk_and_penduduk(self, db: Session, kk_id: UUID, penduduk_id: UUID):
        return (
            db.query(AnggotaKeluarga)
            .filter(
                AnggotaKeluarga.kk_id == kk_id,
                AnggotaKeluarga.penduduk_id == penduduk_id,
            )
            .first()
        )

    def create(self, db: Session, anggota: AnggotaKeluarga):
        db.add(anggota)
        db.commit()
        db.refresh(anggota)

        return anggota

    def delete(self, db: Session, anggota: AnggotaKeluarga):
        db.delete(anggota)
        db.commit()
