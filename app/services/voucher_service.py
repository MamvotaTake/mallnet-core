from datetime import datetime
from typing import List, Optional

from fastapi import HTTPException

from app.repositories.internet_package_repository import InternetPackageRepository
from app.repositories.voucher_repository import VoucherRepository
from app.services.subscription_service import SubscriptionService


class VoucherService:
    def __init__(self, db):
        self.db = db
        self.package_repo = InternetPackageRepository(db)
        self.voucher_repo = VoucherRepository(db)
        self.subscription_service = SubscriptionService(db)

    def create_voucher(
        self,
        mall_id: int,
        package_id: int,
        expires_at: Optional[datetime] = None,
    ):
        package = self.package_repo.get_by_id(package_id)
        if not package:
            raise HTTPException(status_code=404, detail="Internet package not found")

        return self.voucher_repo.create(
            mall_id=mall_id,
            package_id=package.id,
            mikrotik_profile=package.mikrotik_profile,
            duration_days=package.duration_days,
            expires_at=expires_at,
        )

    def bulk_generate(
        self,
        mall_id: int,
        package_id: int,
        quantity: int,
        expires_at: Optional[datetime] = None,
    ) -> List:
        package = self.package_repo.get_by_id(package_id)
        if not package:
            raise HTTPException(status_code=404, detail="Internet package not found")

        if quantity <= 0:
            raise HTTPException(status_code=400, detail="Quantity must be positive")

        return self.voucher_repo.bulk_create(
            mall_id=mall_id,
            package_id=package.id,
            mikrotik_profile=package.mikrotik_profile,
            duration_days=package.duration_days,
            quantity=quantity,
            expires_at=expires_at,
        )

    def get_voucher(self, code: str):
        voucher = self.voucher_repo.get_by_code(code)
        if not voucher:
            raise HTTPException(status_code=404, detail="Voucher not found")
        return voucher

    def list_by_mall(self, mall_id: int):
        return self.voucher_repo.list_by_mall(mall_id)

    def redeem_voucher(
        self,
        mall_id: int,
        mac_address: str,
        code: str,
        pin: str,
    ):
        voucher = self.voucher_repo.get_by_code_and_pin(code=code, pin=pin)
        if not voucher or voucher.mall_id != mall_id:
            raise HTTPException(status_code=404, detail="Voucher not found")

        if voucher.is_used:
            raise HTTPException(status_code=400, detail="Voucher already used")

        if voucher.expires_at and voucher.expires_at < datetime.utcnow():
            raise HTTPException(status_code=400, detail="Voucher expired")

        subscription = self.subscription_service.create_subscription(
            mall_id=mall_id,
            package_id=voucher.package_id,
            mac_address=mac_address,
        )

        self.voucher_repo.mark_used(voucher)
        return subscription
