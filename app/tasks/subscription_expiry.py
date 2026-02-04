from app.tasks.celery_app import celery_app
from app.database.session import SessionLocal
from app.repositories.subscription_repository import SubscriptionRepository
from app.services.subscription_service import SubscriptionService


@celery_app.task
def expire_subscriptions():
    db = SessionLocal()
    try:
        repo = SubscriptionRepository(db)
        service = SubscriptionService(db)

        expired = repo.get_expired_active()

        for subscription in expired:
            service.subscription_repo.deactivate(subscription)
            service._disable_hotspot_user(subscription.user_id)

        return f"Expired {len(expired)} subscriptions"
    finally:
        db.close()
