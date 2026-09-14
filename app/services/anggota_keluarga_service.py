from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.kependudukan import (
    AnggotaKeluarga,
    KartuKeluarga,
    Penduduk
)

from app.repositories.anggota_keluarga_repository import (
    AnggotaKeluargaRepository
)


class AnggotaKeluargaService:

    @staticmethod
    def get_all(db: Session):
        return AnggotaKeluargaRepository.get_all(db)


    @staticmethod
    def get_by_id(
        db: Session,
        anggota_id: UUID
    ):

        anggota = (
            AnggotaKeluargaRepository.get_by_id(
                db,
                anggota_id
            )
        )

        if not anggota:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Anggota keluarga tidak ditemukan"
            )

        return anggota


    @staticmethod
    def get_by_kk_id(
        db: Session,
        kk_id: UUID
    ):

        kk = (
            db.query(KartuKeluarga)
            .filter(
                KartuKeluarga.id == kk_id
            )
            .first()
        )

        if not kk:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Kartu Keluarga tidak ditemukan"
            )

        return (
            AnggotaKeluargaRepository.get_by_kk_id(
                db,
                kk_id
            )
        )


    @staticmethod
    def create(
        db: Session,
        anggota_data
    ):

        # =========================
        # CEK KARTU KELUARGA
        # =========================

        kk = (
            db.query(KartuKeluarga)
            .filter(
                KartuKeluarga.id ==
                anggota_data.kk_id
            )
            .first()
        )

        if not kk:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Kartu Keluarga tidak ditemukan"
            )


        # =========================
        # CEK PENDUDUK
        # =========================

        penduduk = (
            db.query(Penduduk)
            .filter(
                Penduduk.id ==
                anggota_data.penduduk_id
            )
            .first()
        )

        if not penduduk:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Penduduk tidak ditemukan"
            )


        # =========================
        # CEK PENDUDUK SUDAH ADA
        # DI KK LAIN ATAU BELUM
        # =========================

        existing_anggota = (
            AnggotaKeluargaRepository
            .get_by_penduduk_id(
                db,
                anggota_data.penduduk_id
            )
        )

        if existing_anggota:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Penduduk sudah terdaftar "
                    "dalam Kartu Keluarga"
                )
            )


        # =========================
        # BUAT ANGGOTA
        # =========================

        anggota = AnggotaKeluarga(
            kk_id=anggota_data.kk_id,
            penduduk_id=anggota_data.penduduk_id,
            hubungan_keluarga=(
                anggota_data.hubungan_keluarga
            )
        )

        return AnggotaKeluargaRepository.create(
            db,
            anggota
        )


    @staticmethod
    def update(
        db: Session,
        anggota_id: UUID,
        anggota_data
    ):

        anggota = (
            AnggotaKeluargaService.get_by_id(
                db,
                anggota_id
            )
        )

        if anggota_data.hubungan_keluarga is not None:

            anggota.hubungan_keluarga = (
                anggota_data.hubungan_keluarga
            )

        return AnggotaKeluargaRepository.update(
            db,
            anggota
        )


    @staticmethod
    def delete(
        db: Session,
        anggota_id: UUID
    ):

        anggota = (
            AnggotaKeluargaService.get_by_id(
                db,
                anggota_id
            )
        )

        AnggotaKeluargaRepository.delete(
            db,
            anggota
        )

        return {
            "message": (
                "Anggota keluarga berhasil dihapus"
            )
        }