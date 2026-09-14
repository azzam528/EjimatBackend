from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.repositories.penduduk_repository import PendudukRepository
from app.services.duplicate_detection_service import (
    DuplicateDetectionService
)


router = APIRouter(
    prefix="/api/duplicate-check",
    tags=["Duplicate Detection"]
)


@router.get("/penduduk")
def check_duplicate_penduduk(
    nama_lengkap: str,
    tanggal_lahir: date | None = None,
    tempat_lahir: str | None = None,
    db: Session = Depends(get_db)
):

    repository = PendudukRepository()

    class DuplicateCheckData:
        def __init__(
            self,
            nama_lengkap,
            tanggal_lahir,
            tempat_lahir
        ):
            self.nama_lengkap = nama_lengkap
            self.tanggal_lahir = tanggal_lahir
            self.tempat_lahir = tempat_lahir


    data = DuplicateCheckData(
        nama_lengkap=nama_lengkap,
        tanggal_lahir=tanggal_lahir,
        tempat_lahir=tempat_lahir
    )


    possible_duplicates = (
        DuplicateDetectionService.check_penduduk(
            db=db,
            repository=repository,
            data=data
        )
    )


    return {
        "possible_duplicates": possible_duplicates
    }