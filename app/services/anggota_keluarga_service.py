import uuid
from datetime import datetime
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.kependudukan import AnggotaKeluarga, KartuKeluarga, Penduduk

from app.repositories.anggota_keluarga_repository import AnggotaKeluargaRepository

from app.schemas.kependudukan import AnggotaKeluargaCreate


class AnggotaKeluargaService:

    def __init__(self, repository: AnggotaKeluargaRepository | None = None):
        self.repository = repository or AnggotaKeluargaRepository()

    def list_anggota_keluarga(self, db: Session, **filters):
        return self.repository.get_all(db, **filters)

    def get_anggota_keluarga(self, db: Session, anggota_id: UUID):
        anggota = self.repository.get_by_id(db, anggota_id)

        if anggota is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Anggota keluarga not found",
            )

        return anggota

    def create_anggota_keluarga(self, db: Session, data: AnggotaKeluargaCreate):
        # Cek KK
        kk = db.query(KartuKeluarga).filter(KartuKeluarga.id == data.kk_id).first()

        if kk is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Kartu Keluarga not found"
            )

        # Cek Penduduk
        penduduk = db.query(Penduduk).filter(Penduduk.id == data.penduduk_id).first()

        if penduduk is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Penduduk not found"
            )

        # Cek apakah penduduk sudah menjadi anggota
        existing = self.repository.get_by_kk_and_penduduk(
            db, data.kk_id, data.penduduk_id
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Penduduk is already a member of this Kartu Keluarga",
            )

        anggota = AnggotaKeluarga(
            id=uuid.uuid4(),
            kk_id=data.kk_id,
            penduduk_id=data.penduduk_id,
            hubungan_keluarga=data.hubungan_keluarga,
            created_at=datetime.utcnow(),
        )

        return self.repository.create(db, anggota)

    def delete_anggota_keluarga(self, db: Session, anggota_id: UUID):
        anggota = self.get_anggota_keluarga(db, anggota_id)

        self.repository.delete(db, anggota)
