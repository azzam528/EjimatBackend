import json
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.users import AuditLog


class AuditService:
    def add_log(
        self,
        db: Session,
        *,
        user_id: UUID | None,
        action: str,
        module: str,
        table_name: str,
        record_id: UUID | None = None,
        old_data: dict | None = None,
        new_data: dict | None = None,
        ip_address: str | None = None,
    ) -> AuditLog:
        log = AuditLog(
            user_id=user_id,
            action=action,
            module=module,
            table_name=table_name,
            record_id=record_id,
            old_data=(
                json.dumps(old_data, ensure_ascii=False, default=str)
                if old_data is not None
                else None
            ),
            new_data=(
                json.dumps(new_data, ensure_ascii=False, default=str)
                if new_data is not None
                else None
            ),
            ip_address=ip_address,
        )

        # Tidak commit di sini. Log ikut transaksi
        # yang di-commit oleh operasi utama.
        db.add(log)
        return log


audit_service = AuditService()
