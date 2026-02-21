from datetime import date, datetime
from typing import List, Optional, Type

from sqlalchemy import text
from sqlalchemy.orm import Session
from app.models.subscription import Subscription
from app.repositories.base import BaseRepository

class SubscriptionRepository(BaseRepository):

    def create(
        self,
        user_id: int,
        package_id: int,
        start_date,
        end_date,
        is_active: bool = True,
    ):
        subscription = Subscription(
            user_id=user_id,
            package_id=package_id,
            start_date=start_date,
            end_date=end_date,
            is_active=is_active,
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
                Subscription.end_date < date.utcnow(),
            )
            .all()
        )

    def exists_today(self, user_id: int, package_id: int) -> bool:
        today = date.today()
        return self.db.query(Subscription).filter(
            Subscription.user_id == user_id,
            Subscription.package_id == package_id,
            Subscription.start_date >= today
        ).first() is not None

    def log_action(self, subscription_id: int, action: str, notes: str = None):
        self.db.execute(
            text("""
                INSERT INTO subscription_audit_logs
                (subscription_id, action, notes)
                VALUES (:subscription_id, :action, :notes)
            """),
            {
                "subscription_id": subscription_id,
                "action": action,
                "notes": notes,
            }
        )
        self.db.commit()