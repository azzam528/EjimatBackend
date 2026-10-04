import uuid
from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.kependudukan import Penduduk
from app.models.pengaduan import Pengaduan

from app.repositories.pengaduan_repository import (
    PengaduanRepository,
)

from app.schemas.pengaduan import (
    PengaduanCreate,
    PengaduanUpdate,
)


class PengaduanService:

    def __init__(
        self,
        repository: PengaduanRepository | None = None,
    ):
        self.repository = repository or PengaduanRepository()

    def list_pengaduan(
        self,
        db: Session,
        **filters,
    ):
        return self.repository.get_all(
            db,
            **filters,
        )

    def get_pengaduan(
        self,
        db: Session,
        pengaduan_id,
    ):
        pengaduan = self.repository.get_by_id(
            db,
            pengaduan_id,
        )

        if pengaduan is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pengaduan not found",
            )

        return pengaduan

    def create_pengaduan(
        self,
        db: Session,
        data: PengaduanCreate,
    ):

        penduduk = db.query(Penduduk).filter(Penduduk.id == data.penduduk_id).first()

        if penduduk is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Penduduk not found",
            )

        now = datetime.utcnow()

        pengaduan = Pengaduan(
            id=uuid.uuid4(),
            penduduk_id=data.penduduk_id,
            judul=data.judul,
            deskripsi=data.deskripsi,
            status="diajukan",
            tanggal_pengaduan=now,
            created_at=now,
        )

        return self.repository.create(
            db,
            pengaduan,
        )

    def update_pengaduan(
        self,
        db: Session,
        pengaduan_id,
        data: PengaduanUpdate,
    ):

        pengaduan = self.get_pengaduan(
            db,
            pengaduan_id,
        )

        update_data = data.model_dump(exclude_unset=True)

        if "status" in update_data:

            allowed_status = {
                "diajukan",
                "diproses",
                "selesai",
                "ditolak",
            }

            new_status = update_data["status"]

            if new_status not in allowed_status:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={
                        "message": "Invalid status",
                        "allowed_status": list(allowed_status),
                    },
                )

            pengaduan.status = new_status

        if "catatan_petugas" in update_data:
            pengaduan.catatan_petugas = update_data["catatan_petugas"]

        pengaduan.updated_at = datetime.utcnow()

        return self.repository.update(
            db,
            pengaduan,
        )
