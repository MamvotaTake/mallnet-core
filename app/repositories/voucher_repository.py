import secrets
from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.voucher import Voucher


class VoucherRepository:
    def __init__(self, db: Session):
        self.db = db

    def _generate_code_pin(self) -> tuple:
        code = secrets.token_hex(4).upper()
        pin = str(secrets.randbelow(9000) + 1000)
        return code, pin

    def _unique_code_pin(self) -> tuple:
        for _ in range(10):
            code, pin = self._generate_code_pin()
            if not self.get_by_code(code):
                return code, pin
        raise ValueError("Unable to generate unique voucher code")

    def create(
        self,
        mall_id: int,
        package_id: int,
        mikrotik_profile: str,
        duration_days: int,
        expires_at: Optional[datetime] = None,
    ) -> Voucher:
        code, pin = self._unique_code_pin()

        voucher = Voucher(
            code=code,
            pin=pin,
            mall_id=mall_id,
            package_id=package_id,
            mikrotik_profile=mikrotik_profile,
            duration_days=duration_days,
            expires_at=expires_at,
        )

        self.db.add(voucher)
        self.db.commit()
        self.db.refresh(voucher)
        return voucher

    def bulk_create(
        self,
        mall_id: int,
        package_id: int,
        mikrotik_profile: str,
        duration_days: int,
        quantity: int,
        expires_at: Optional[datetime] = None,
    ) -> List[Voucher]:
        vouchers = []
        existing_codes = set()
        for _ in range(quantity):
            code, pin = self._generate_code_pin()
            while code in existing_codes:
                code, pin = self._generate_code_pin()
            existing_codes.add(code)
            vouchers.append(
                Voucher(
                    code=code,
                    pin=pin,
                    mall_id=mall_id,
                    package_id=package_id,
                    mikrotik_profile=mikrotik_profile,
                    duration_days=duration_days,
                    expires_at=expires_at,
                )
            )

        self.db.add_all(vouchers)
        self.db.commit()
        for voucher in vouchers:
            self.db.refresh(voucher)
        return vouchers

    def get_by_code(self, code: str) -> Optional[Voucher]:
        return (
            self.db.query(Voucher)
            .filter(Voucher.code == code)
            .first()
        )

    def get_by_code_and_pin(self, code: str, pin: str) -> Optional[Voucher]:
        return (
            self.db.query(Voucher)
            .filter(
                Voucher.code == code,
                Voucher.pin == pin,
            )
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
