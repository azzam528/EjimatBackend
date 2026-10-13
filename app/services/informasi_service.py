import re
import uuid
from datetime import datetime
from typing import Type

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.informasi import Berita, Pengumuman
from app.models.users import User

ALLOWED_STATUS = {"draft", "published", "archived"}


class InformasiService:
    def _get_model(self, jenis: str):
        if jenis == "berita":
            return Berita
        if jenis == "pengumuman":
            return Pengumuman
        raise HTTPException(status_code=404, detail="Jenis informasi tidak ditemukan")

    def list_items(
        self,
        db: Session,
        jenis: str,
        status_filter: str | None = "published",
        skip: int = 0,
        limit: int = 20,
    ):
        model = self._get_model(jenis)
        query = db.query(model)

        if status_filter is not None:
            query = query.filter(model.status == status_filter)

        return query.order_by(model.created_at.desc()).offset(skip).limit(limit).all()

    def get_item(self, db: Session, jenis: str, item_id: uuid.UUID):
        model = self._get_model(jenis)
        item = db.query(model).filter(model.id == item_id).first()

        if item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{jenis.capitalize()} tidak ditemukan",
            )

        return item

    def create_item(self, db: Session, jenis: str, data):
        model = self._get_model(jenis)
        payload = data.model_dump()
        author_id = payload.get("author_id")

        if author_id is not None:
            author = db.query(User).filter(User.id == author_id).first()
            if author is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Author tidak ditemukan",
                )

        item_status = payload.get("status", "draft")
        self._validate_status(item_status)

        now = datetime.utcnow()
        payload["id"] = uuid.uuid4()
        payload["created_at"] = now
        payload["updated_at"] = now
        payload["published_at"] = now if item_status == "published" else None

        if jenis == "berita":
            payload["slug"] = self._slugify(payload["judul"])

        item = model(**payload)

        try:
            db.add(item)
            db.commit()
            db.refresh(item)
            return item
        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Gagal menyimpan informasi ke database",
            )

    def update_item(
        self,
        db: Session,
        jenis: str,
        item_id: uuid.UUID,
        data,
    ):
        item = self.get_item(db, jenis, item_id)
        payload = data.model_dump(exclude_unset=True)

        if "status" in payload and payload["status"] is not None:
            self._validate_status(payload["status"])

        for field, value in payload.items():
            setattr(item, field, value)

        if jenis == "berita" and "judul" in payload:
            item.slug = self._slugify(item.judul or "")

        if "status" in payload:
            if payload["status"] == "published" and item.published_at is None:
                item.published_at = datetime.utcnow()
            elif payload["status"] != "published":
                item.published_at = None

        item.updated_at = datetime.utcnow()

        try:
            db.commit()
            db.refresh(item)
            return item
        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Gagal memperbarui informasi di database",
            )

    def delete_item(self, db: Session, jenis: str, item_id: uuid.UUID):
        item = self.get_item(db, jenis, item_id)

        try:
            db.delete(item)
            db.commit()
            return {"message": f"{jenis.capitalize()} berhasil dihapus"}
        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Gagal menghapus informasi dari database",
            )

    @staticmethod
    def _validate_status(value: str):
        if value not in ALLOWED_STATUS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": "Status tidak valid",
                    "allowed_status": sorted(ALLOWED_STATUS),
                },
            )

    @staticmethod
    def _slugify(value: str) -> str:
        slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
        return slug[:220] or "berita"
