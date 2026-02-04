from celery.schedules import crontab
from app.tasks.celery_app import celery_app

celery_app.conf.beat_schedule = {
    "expire-subscriptions-every-5-minutes": {
        "task": "app.tasks.subscription_expiry.expire_subscriptions",
        "schedule": crontab(minute="*/5"),
    },
}
