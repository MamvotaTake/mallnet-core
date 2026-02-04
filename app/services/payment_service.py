from sqlalchemy.orm import Session
from app.repositories.payment_repository import PaymentRepository
from app.repositories.internet_package_repository import InternetPackageRepository
from app.services.subscription_service import SubscriptionService
from typing import Optional

class PaymentService:
    def __init__(self, db: Session):
        self.db = db
        self.payment_repo = PaymentRepository(db)
        self.package_repo = InternetPackageRepository(db)
        self.subscription_service = SubscriptionService(db)

    def process_payment(
        self,
        user_id: int,
        package_id: int,
        method: str,
        reference: Optional[str] = None
    ):
        package = self.package_repo.get_by_id(package_id)
        if not package:
            raise ValueError("Invalid package")

        # 1️⃣ Record payment
        payment = self.payment_repo.create(
            user_id=user_id,
            package_id=package_id,
            amount=package.price,
            method=method,
            reference=reference,
        )

        # 2️⃣ Activate subscription (this enables MikroTik)
        subscription = self.subscription_service.create_subscription(
            user_id=user_id,
            package_id=package_id,
        )

        return {
            "payment": payment,
            "subscription": subscription,
        }
