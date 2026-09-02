from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database.database import get_db

router = APIRouter()

@router.get("")
def health_check():
    return {"status": "ok"}

@router.get("/db")
def health_check_db(db: Session = Depends(get_db)):
    try:
        # Try to execute a simple query to check the database connection
        db.execute(text("SELECT 1"))
        return {"status": "database ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")
