from uuid import UUID
from sqlalchemy.orm import Session

from app.models.wilayah import Dusun, RW, RT


# =========================
# DUSUN
# =========================

def get_all_dusun(db: Session):
    return db.query(Dusun).all()


def get_dusun_by_id(db: Session, dusun_id: UUID):
    return db.query(Dusun).filter(Dusun.id == dusun_id).first()


def create_dusun(db: Session, dusun_data):
    dusun = Dusun(
        name=dusun_data.name,
        code=dusun_data.code
    )

    db.add(dusun)
    db.commit()
    db.refresh(dusun)

    return dusun


def delete_dusun(db: Session, dusun: Dusun):
    db.delete(dusun)
    db.commit()


# =========================
# RW
# =========================

def get_all_rw(db: Session):
    return db.query(RW).all()


def get_rw_by_id(db: Session, rw_id: UUID):
    return db.query(RW).filter(RW.id == rw_id).first()


def get_rw_by_dusun_id(db: Session, dusun_id: UUID):
    return db.query(RW).filter(RW.dusun_id == dusun_id).all()


def create_rw(db: Session, rw_data):
    rw = RW(
        dusun_id=rw_data.dusun_id,
        number=rw_data.number,
        code=rw_data.code
    )

    db.add(rw)
    db.commit()
    db.refresh(rw)

    return rw


def delete_rw(db: Session, rw: RW):
    db.delete(rw)
    db.commit()


# =========================
# RT
# =========================

def get_all_rt(db: Session):
    return db.query(RT).all()


def get_rt_by_id(db: Session, rt_id: UUID):
    return db.query(RT).filter(RT.id == rt_id).first()


def get_rt_by_rw_id(db: Session, rw_id: UUID):
    return db.query(RT).filter(RT.rw_id == rw_id).all()


def create_rt(db: Session, rt_data):
    rt = RT(
        rw_id=rt_data.rw_id,
        number=rt_data.number,
        code=rt_data.code
    )

    db.add(rt)
    db.commit()
    db.refresh(rt)

    return rt


def delete_rt(db: Session, rt: RT):
    db.delete(rt)
    db.commit()