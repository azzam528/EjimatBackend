import uuid
from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.kependudukan import Penduduk
from app.models.pengaduan import Pengaduan
from app.models.wilayah import RT

from app.repositories.pengaduan_repository import PengaduanRepository
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
        # Validasi penduduk
        penduduk = db.query(Penduduk).filter(Penduduk.id == data.penduduk_id).first()

        if penduduk is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Penduduk not found",
            )

        # Validasi RT jika diberikan
        if data.rt_id is not None:
            rt = db.query(RT).filter(RT.id == data.rt_id).first()

            if rt is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="RT not found",
                )

        now = datetime.utcnow()

        # Generate nomor pengaduan
        nomor_pengaduan = (
            f"PG-{now.strftime('%Y%m%d%H%M%S')}-" f"{uuid.uuid4().hex[:6].upper()}"
        )

        pengaduan = Pengaduan(
            id=uuid.uuid4(),
            penduduk_id=data.penduduk_id,
            rt_id=data.rt_id,
            nomor_pengaduan=nomor_pengaduan,
            kategori=data.kategori,
            judul=data.judul,
            deskripsi=data.deskripsi,
            lokasi=data.lokasi,
            latitude=data.latitude,
            longitude=data.longitude,
            status="diajukan",
            created_at=now,
            updated_at=now,
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

        # Validasi status
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

        # Validasi RT jika diubah
        if "rt_id" in update_data and update_data["rt_id"] is not None:
            rt = db.query(RT).filter(RT.id == update_data["rt_id"]).first()

            if rt is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="RT not found",
                )

        # Update field
        for field, value in update_data.items():
            setattr(
                pengaduan,
                field,
                value,
            )

        now = datetime.utcnow()

        pengaduan.updated_at = now

        # Jika selesai, isi selesai_at
        if "status" in update_data and update_data["status"] == "selesai":
            pengaduan.selesai_at = now

        # Jika status berubah dari selesai
        elif "status" in update_data and update_data["status"] != "selesai":
            pengaduan.selesai_at = None

        return self.repository.update(
            db,
            pengaduan,
        )
