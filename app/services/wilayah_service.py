from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories import wilayah_repository


# =========================
# DUSUN
# =========================

def get_all_dusun(db: Session):
    return wilayah_repository.get_all_dusun(db)


def get_dusun_by_id(db: Session, dusun_id: UUID):
    dusun = wilayah_repository.get_dusun_by_id(db, dusun_id)

    if not dusun:
        raise HTTPException(
            status_code=404,
            detail="Dusun tidak ditemukan"
        )

    return dusun


def create_dusun(db: Session, dusun_data):
    return wilayah_repository.create_dusun(
        db,
        dusun_data
    )


def delete_dusun(db: Session, dusun_id: UUID):
    dusun = get_dusun_by_id(db, dusun_id)

    wilayah_repository.delete_dusun(
        db,
        dusun
    )

    return {
        "message": "Dusun berhasil dihapus"
    }


# =========================
# RW
# =========================

def get_all_rw(db: Session):
    return wilayah_repository.get_all_rw(db)


def get_rw_by_id(db: Session, rw_id: UUID):
    rw = wilayah_repository.get_rw_by_id(db, rw_id)

    if not rw:
        raise HTTPException(
            status_code=404,
            detail="RW tidak ditemukan"
        )

    return rw


def get_rw_by_dusun_id(db: Session, dusun_id: UUID):
    return wilayah_repository.get_rw_by_dusun_id(
        db,
        dusun_id
    )


def create_rw(db: Session, rw_data):

    dusun = wilayah_repository.get_dusun_by_id(
        db,
        rw_data.dusun_id
    )

    if not dusun:
        raise HTTPException(
            status_code=404,
            detail="Dusun tidak ditemukan"
        )

    return wilayah_repository.create_rw(
        db,
        rw_data
    )


def delete_rw(db: Session, rw_id: UUID):

    rw = get_rw_by_id(db, rw_id)

    wilayah_repository.delete_rw(
        db,
        rw
    )

    return {
        "message": "RW berhasil dihapus"
    }


# =========================
# RT
# =========================

def get_all_rt(db: Session):
    return wilayah_repository.get_all_rt(db)


def get_rt_by_id(db: Session, rt_id: UUID):
    rt = wilayah_repository.get_rt_by_id(db, rt_id)

    if not rt:
        raise HTTPException(
            status_code=404,
            detail="RT tidak ditemukan"
        )

    return rt


def get_rt_by_rw_id(db: Session, rw_id: UUID):
    return wilayah_repository.get_rt_by_rw_id(
        db,
        rw_id
    )


def create_rt(db: Session, rt_data):

    rw = wilayah_repository.get_rw_by_id(
        db,
        rt_data.rw_id
    )

    if not rw:
        raise HTTPException(
            status_code=404,
            detail="RW tidak ditemukan"
        )

    return wilayah_repository.create_rt(
        db,
        rt_data
    )


def delete_rt(db: Session, rt_id: UUID):

    rt = get_rt_by_id(db, rt_id)

    wilayah_repository.delete_rt(
        db,
        rt
    )

    return {
        "message": "RT berhasil dihapus"
    }