import os
import uuid
from datetime import datetime
from pathlib import Path

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.models.layanan import DokumenPengajuan, PengajuanLayanan
from app.repositories.dokumen_pengajuan_repository import (
    DokumenPengajuanRepository,
)


UPLOAD_DIR = Path("uploads/pengajuan_layanan")

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".jpg",
    ".jpeg",
    ".png",
    ".doc",
    ".docx",
}

MAX_FILE_SIZE = 10 * 1024 * 1024


class DokumenPengajuanService:

    def __init__(
        self,
        repository: DokumenPengajuanRepository | None = None,
    ):
        self.repository = repository or DokumenPengajuanRepository()

    def list_dokumen(
        self,
        db: Session,
        pengajuan_id,
    ):
        pengajuan = (
            db.query(PengajuanLayanan)
            .filter(PengajuanLayanan.id == pengajuan_id)
            .first()
        )

        if pengajuan is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pengajuan layanan not found",
            )

        return self.repository.get_all_by_pengajuan(
            db,
            pengajuan_id,
        )

    def get_dokumen(
        self,
        db: Session,
        dokumen_id,
    ):
        dokumen = self.repository.get_by_id(
            db,
            dokumen_id,
        )

        if dokumen is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Dokumen pengajuan not found",
            )

        return dokumen

    async def upload_dokumen(
        self,
        db: Session,
        pengajuan_id,
        file: UploadFile,
    ):
        pengajuan = (
            db.query(PengajuanLayanan)
            .filter(PengajuanLayanan.id == pengajuan_id)
            .first()
        )

        if pengajuan is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pengajuan layanan not found",
            )

        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Filename is required",
            )

        original_filename = file.filename
        extension = Path(original_filename).suffix.lower()

        if extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": "File type is not allowed",
                    "allowed_extensions": sorted(ALLOWED_EXTENSIONS),
                },
            )

        file_content = await file.read()

        if len(file_content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File size must not exceed 10 MB",
            )

        UPLOAD_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        generated_filename = f"{uuid.uuid4()}{extension}"

        file_path = UPLOAD_DIR / generated_filename

        with open(file_path, "wb") as buffer:
            buffer.write(file_content)

        now = datetime.utcnow()

        dokumen = DokumenPengajuan(
            id=uuid.uuid4(),
            pengajuan_id=pengajuan_id,
            nama_dokumen=original_filename,
            file_path=str(file_path),
            file_type=file.content_type,
            file_size=len(file_content),
            uploaded_at=now,
        )

        try:
            return self.repository.create(
                db,
                dokumen,
            )

        except Exception:
            if file_path.exists():
                os.remove(file_path)

            raise

    def delete_dokumen(
        self,
        db: Session,
        dokumen_id,
    ):
        dokumen = self.get_dokumen(
            db,
            dokumen_id,
        )

        file_path = Path(dokumen.file_path)

        self.repository.delete(
            db,
            dokumen,
        )

        if file_path.exists():
            file_path.unlink()

        return {
            "message": "Dokumen pengajuan deleted successfully"
        }