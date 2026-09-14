from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.kependudukan import KartuKeluarga, Penduduk
from app.models.wilayah import RT

from app.repositories.kartu_keluarga_repository import (
    KartuKeluargaRepository
)


class KartuKeluargaService:

    @staticmethod
    def get_all(db: Session):
        return KartuKeluargaRepository.get_all(db)


    @staticmethod
    def get_by_id(db: Session, kk_id: UUID):

        kk = KartuKeluargaRepository.get_by_id(
            db,
            kk_id
        )

        if not kk:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Kartu Keluarga tidak ditemukan"
            )

        return kk


    @staticmethod
    def create(db: Session, kk_data):

        # Cek nomor KK sudah ada atau belum
        existing_kk = KartuKeluargaRepository.get_by_no_kk(
            db,
            kk_data.no_kk
        )

        if existing_kk:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nomor Kartu Keluarga sudah terdaftar"
            )

        # Cek RT
        rt = (
            db.query(RT)
            .filter(RT.id == kk_data.rt_id)
            .first()
        )

        if not rt:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="RT tidak ditemukan"
            )

        # Cek kepala keluarga
        kepala_keluarga = (
            db.query(Penduduk)
            .filter(
                Penduduk.id == kk_data.kepala_keluarga_id
            )
            .first()
        )

        if not kepala_keluarga:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Penduduk sebagai kepala keluarga tidak ditemukan"
            )

        kk = KartuKeluarga(
            no_kk=kk_data.no_kk,
            kepala_keluarga_id=kk_data.kepala_keluarga_id,
            alamat=kk_data.alamat,
            rt_id=kk_data.rt_id
        )

        return KartuKeluargaRepository.create(
            db,
            kk
        )


    @staticmethod
    def update(
        db: Session,
        kk_id: UUID,
        kk_data
    ):

        kk = KartuKeluargaService.get_by_id(
            db,
            kk_id
        )

        # Jika nomor KK diubah
        if (
            kk_data.no_kk is not None
            and kk_data.no_kk != kk.no_kk
        ):

            existing_kk = (
                KartuKeluargaRepository.get_by_no_kk(
                    db,
                    kk_data.no_kk
                )
            )

            if existing_kk:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Nomor Kartu Keluarga sudah digunakan"
                )

            kk.no_kk = kk_data.no_kk


        # Jika kepala keluarga diubah
        if kk_data.kepala_keluarga_id is not None:

            penduduk = (
                db.query(Penduduk)
                .filter(
                    Penduduk.id ==
                    kk_data.kepala_keluarga_id
                )
                .first()
            )

            if not penduduk:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Penduduk tidak ditemukan"
                )

            kk.kepala_keluarga_id = (
                kk_data.kepala_keluarga_id
            )


        # Jika alamat diubah
        if kk_data.alamat is not None:
            kk.alamat = kk_data.alamat


        # Jika RT diubah
        if kk_data.rt_id is not None:

            rt = (
                db.query(RT)
                .filter(RT.id == kk_data.rt_id)
                .first()
            )

            if not rt:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="RT tidak ditemukan"
                )

            kk.rt_id = kk_data.rt_id


        return KartuKeluargaRepository.update(
            db,
            kk
        )


    @staticmethod
    def delete(
        db: Session,
        kk_id: UUID
    ):

        kk = KartuKeluargaService.get_by_id(
            db,
            kk_id
        )

        KartuKeluargaRepository.delete(
            db,
            kk
        )

        return {
            "message": "Kartu Keluarga berhasil dihapus"
        }