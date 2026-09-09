from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database.database import get_db


router = APIRouter(
    prefix="/api/health",
    tags=["Health"]
)


@router.get("")
def health_check():
    return {
        "status": "ok",
        "message": "EJIMAT Backend is running"
    }


@router.get("/db")
def database_health(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))

        return {
            "status": "ok",
            "database": "connected"
        }

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Database disconnected"
        )


@router.get("/info")
def application_info():
    return {
        "application": "EJIMAT Core Desa Cimenyan",
        "status": "running"
    }