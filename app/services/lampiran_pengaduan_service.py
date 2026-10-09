```python
import os
import uuid
from datetime import datetime
from pathlib import Path

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.models.pengaduan import (
    Pengaduan,
    LampiranPengaduan,
)
from app.repositories.lampiran_pengaduan_repository import (
    LampiranPengaduanRepository,
)


UPLOAD_DIR = Path("uploads/pengaduan")

ALLOWED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".pdf",
}

MAX_FILE_SIZE = 10 * 1024 * 1024


class LampiranPengaduanService:

    def __init__(
        self,
        repository: LampiranPengaduanRepository | None = None,
    ):
        self.repository = repository or LampiranPengaduanRepository()

    def list_lampiran(
        self,
        db: Session,
        pengaduan_id,
    ):
        pengaduan = (
            db.query(Pengaduan)
            .filter(Pengaduan.id == pengaduan_id)
            .first()
        )

        if pengaduan is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pengaduan not found",
            )

        return self.repository.get_all_by_pengaduan(
            db,
            pengaduan_id,
        )

    def get_lampiran(
        self,
        db: Session,
        lampiran_id,
    ):
        lampiran = self.repository.get_by_id(
            db,
            lampiran_id,
        )

        if lampiran is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Lampiran pengaduan not found",
            )

        return lampiran

    async def upload_lampiran(
        self,
        db: Session,
        pengaduan_id,
        file: UploadFile,
    ):
        pengaduan = (
            db.query(Pengaduan)
            .filter(Pengaduan.id == pengaduan_id)
            .first()
        )

        if pengaduan is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pengaduan not found",
            )

        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Filename is required",
            )

        extension = Path(file.filename).suffix.lower()

        if extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": "File type is not allowed",
                    "allowed_extensions": sorted(ALLOWED_EXTENSIONS),
                },
            )

        # Baca maksimal 1 byte di atas batas untuk mendeteksi file terlalu besar.
        file_content = await file.read(MAX_FILE_SIZE + 1)

        if len(file_content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="File size must not exceed 10 MB",
            )

        if not file_content:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File cannot be empty",
            )

        UPLOAD_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        generated_filename = f"{uuid.uuid4()}{extension}"
        file_path = UPLOAD_DIR / generated_filename

        try:
            with file_path.open("wb") as buffer:
                buffer.write(file_content)

            lampiran = LampiranPengaduan(
                id=uuid.uuid4(),
                pengaduan_id=pengaduan_id,
                file_path=str(file_path),
                file_type=file.content_type,
                created_at=datetime.utcnow(),
            )

            return self.repository.create(
                db,
                lampiran,
            )

        except Exception:
            if file_path.exists():
                file_path.unlink()

            raise

        finally:
            await file.close()

    def delete_lampiran(
        self,
        db: Session,
        lampiran_id,
    ):
        lampiran = self.get_lampiran(
            db,
            lampiran_id,
        )

        file_path = Path(lampiran.file_path)

        self.repository.delete(
            db,
            lampiran,
        )

        if file_path.exists():
            file_path.unlink()

        return {
            "message": "Lampiran pengaduan deleted successfully"
        }
```