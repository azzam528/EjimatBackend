import uuid
from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.layanan import (
    JenisLayanan,
    PengajuanLayanan,
)
from app.models.kependudukan import Penduduk

from app.repositories.pengajuan_layanan_repository import (
    PengajuanLayananRepository,
)

from app.schemas.layanan import (
    PengajuanLayananCreate,
    PengajuanLayananUpdate,
)


class PengajuanLayananService:

    def __init__(self, repository: PengajuanLayananRepository | None = None):
        self.repository = repository or PengajuanLayananRepository()

    def list_pengajuan_layanan(self, db: Session, **filters):
        return self.repository.get_all(db, **filters)

    def get_pengajuan_layanan(self, db: Session, pengajuan_id):
        pengajuan = self.repository.get_by_id(db, pengajuan_id)

        if pengajuan is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pengajuan layanan not found",
            )

        return pengajuan

    def create_pengajuan_layanan(self, db: Session, data: PengajuanLayananCreate):

        # =========================
        # 1. CEK JENIS LAYANAN
        # =========================

        jenis_layanan = (
            db.query(JenisLayanan)
            .filter(JenisLayanan.id == data.jenis_layanan_id)
            .first()
        )

        if jenis_layanan is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Jenis layanan not found"
            )

        # Pastikan layanan masih aktif
        if not jenis_layanan.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Jenis layanan is not active",
            )

        # =========================
        # 2. CEK PENDUDUK
        # =========================

        penduduk = db.query(Penduduk).filter(Penduduk.id == data.penduduk_id).first()

        if penduduk is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Penduduk not found"
            )

        # =========================
        # 3. GENERATE NOMOR
        # =========================

        nomor_pengajuan = self.generate_nomor_pengajuan()

        # =========================
        # 4. BUAT PENGAJUAN
        # =========================

        now = datetime.utcnow()

        pengajuan = PengajuanLayanan(
            id=uuid.uuid4(),
            jenis_layanan_id=data.jenis_layanan_id,
            penduduk_id=data.penduduk_id,
            nomor_pengajuan=nomor_pengajuan,
            status="diajukan",
            catatan_pemohon=data.catatan_pemohon,
            diajukan_at=now,
            created_at=now,
        )

        return self.repository.create(db, pengajuan)

    def update_pengajuan_layanan(
        self, db: Session, pengajuan_id, data: PengajuanLayananUpdate
    ):

        pengajuan = self.get_pengajuan_layanan(db, pengajuan_id)

        update_data = data.model_dump(exclude_unset=True)

        if "status" in update_data:

            new_status = update_data["status"]

            allowed_status = {
                "diajukan",
                "diproses",
                "selesai",
                "ditolak",
            }

            if new_status not in allowed_status:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={
                        "message": "Invalid status",
                        "allowed_status": list(allowed_status),
                    },
                )

            pengajuan.status = new_status

            if new_status == "selesai":
                pengajuan.selesai_at = datetime.utcnow()

        if "catatan_petugas" in update_data:
            pengajuan.catatan_petugas = update_data["catatan_petugas"]

        pengajuan.updated_at = datetime.utcnow()

        return self.repository.update(db, pengajuan)

    @staticmethod
    def generate_nomor_pengajuan():

        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")

        random_part = str(uuid.uuid4())[:6].upper()

        return f"PL-{timestamp}-{random_part}"
