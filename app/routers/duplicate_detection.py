from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.services.duplicate_detection_service import (
    DuplicateDetectionService
)


router = APIRouter(
    prefix="/api/duplicate-check",
    tags=["Duplicate Detection"]
)


@router.get("/penduduk")
def check_duplicate_penduduk(
    nama: str,
    tanggal_lahir: date = None,
    tempat_lahir: str = None,
    db: Session = Depends(get_db)
):

    return {
        "possible_duplicates":
            DuplicateDetectionService.check_penduduk(
                db=db,
                nama=nama,
                tanggal_lahir=tanggal_lahir,
                tempat_lahir=tempat_lahir
            )
    }