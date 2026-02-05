from app.tasks.celery_app import celery_app
from app.database.session import SessionLocal
from app.services.subscription_service import SubscriptionService


@celery_app.task
def expire_subscriptions():
    db = SessionLocal()
    try:
        service = SubscriptionService(db)
        count = service.expire_subscriptions()

        return f"Expired {count} subscriptions"
    finally:
        db.close()
