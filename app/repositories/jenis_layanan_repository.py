from uuid import UUID

from sqlalchemy.orm import Session

from app.models.layanan import JenisLayanan


class JenisLayananRepository:

    def get_all(self, db: Session):
        return db.query(JenisLayanan).order_by(JenisLayanan.nama_layanan.asc()).all()

    def get_by_id(self, db: Session, layanan_id: UUID):
        return db.query(JenisLayanan).filter(JenisLayanan.id == layanan_id).first()

    def get_by_nama(self, db: Session, nama_layanan: str):
        return (
            db.query(JenisLayanan)
            .filter(JenisLayanan.nama_layanan == nama_layanan)
            .first()
        )

    def create(self, db: Session, jenis_layanan: JenisLayanan):
        db.add(jenis_layanan)
        db.commit()
        db.refresh(jenis_layanan)

        return jenis_layanan

    def update(self, db: Session, jenis_layanan: JenisLayanan):
        db.commit()
        db.refresh(jenis_layanan)

        return jenis_layanan

    def delete(self, db: Session, jenis_layanan: JenisLayanan):
        db.delete(jenis_layanan)
        db.commit()
