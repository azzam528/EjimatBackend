from uuid import UUID

from sqlalchemy.orm import Session

from app.models.layanan import PengajuanLayanan


class PengajuanLayananRepository:

    def get_all(
        self,
        db: Session,
        jenis_layanan_id: UUID | None = None,
        penduduk_id: UUID | None = None,
        status: str | None = None,
        skip: int = 0,
        limit: int = 100,
    ):
        query = db.query(PengajuanLayanan)

        if jenis_layanan_id is not None:
            query = query.filter(PengajuanLayanan.jenis_layanan_id == jenis_layanan_id)

        if penduduk_id is not None:
            query = query.filter(PengajuanLayanan.penduduk_id == penduduk_id)

        if status is not None:
            query = query.filter(PengajuanLayanan.status == status)

        return (
            query.order_by(PengajuanLayanan.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_id(self, db: Session, pengajuan_id: UUID):
        return (
            db.query(PengajuanLayanan)
            .filter(PengajuanLayanan.id == pengajuan_id)
            .first()
        )

    def get_by_nomor(self, db: Session, nomor_pengajuan: str):
        return (
            db.query(PengajuanLayanan)
            .filter(PengajuanLayanan.nomor_pengajuan == nomor_pengajuan)
            .first()
        )

    def create(self, db: Session, pengajuan: PengajuanLayanan):
        db.add(pengajuan)
        db.commit()
        db.refresh(pengajuan)

        return pengajuan

    def update(self, db: Session, pengajuan: PengajuanLayanan):
        db.commit()
        db.refresh(pengajuan)

        return pengajuan
