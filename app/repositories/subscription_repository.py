from datetime import datetime
from typing import List, Optional, Type
from sqlalchemy.orm import Session
from app.models.subscription import Subscription
from app.repositories.base import BaseRepository

class SubscriptionRepository(BaseRepository):

    def create(self, user_id: int, package_id: int, end_date):
        subscription = Subscription(
            user_id=user_id,
            package_id=package_id,
            start_date=datetime.utcnow(),
            end_date=end_date,
            is_active=True,
        )
        self.db.add(subscription)
        self.db.commit()
        self.db.refresh(subscription)
        return subscription

    def get_all(self) -> List[Type[Subscription]]:
        return self.db.query(Subscription).all()

    def get_active_by_user(self, user_id: int) -> Optional[Subscription]:
        return (
            self.db.query(Subscription)
            .filter(
                Subscription.user_id == user_id,
                Subscription.is_active == True,
            )
            .first()
        )

    def deactivate(self, subscription: Subscription) -> Subscription:
        subscription.is_active = False
        self.db.commit()
        self.db.refresh(subscription)
        return subscription

    def get_expired_active(self) -> List[Type[Subscription]]:
        return (
            self.db.query(Subscription)
            .filter(
                Subscription.is_active == True,
                Subscription.end_date < datetime.utcnow(),
            )
            .all()
        )