from __future__ import annotations

import secrets
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.voucher import Voucher


class VoucherRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, mall_id: int, package_id: int, expires_at=None) -> Voucher:
        code = secrets.token_urlsafe(8)

        voucher = Voucher(
            code=code,
            mall_id=mall_id,
            package_id=package_id,
            expires_at=expires_at,
        )

        self.db.add(voucher)
        self.db.commit()
        self.db.refresh(voucher)
        return voucher

    def get_by_code(self, code: str) -> Voucher | None:
        return (
            self.db.query(Voucher)
            .filter(Voucher.code == code)
            .first()
        )

    def mark_used(self, voucher: Voucher):
        voucher.is_used = True
        voucher.used_at = datetime.utcnow()
        self.db.commit()

    def list_by_mall(self, mall_id: int):
        return (
            self.db.query(Voucher)
            .filter(Voucher.mall_id == mall_id)
            .all()
        )
