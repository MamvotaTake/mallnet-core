from app.models.payment import Payment
from app.repositories.base import BaseRepository
from typing import Optional

class PaymentRepository(BaseRepository):

    def create(
        self,
        user_id: int,
        package_id: int,
        amount: float,
        method: str,
        reference: Optional[str] = None
    ) -> Payment:
        payment = Payment(
            user_id=user_id,
            package_id=package_id,
            amount=amount,
            method=method,
            reference=reference,
        )
        self.db.add(payment)
        self.db.commit()
        self.db.refresh(payment)
        return payment
