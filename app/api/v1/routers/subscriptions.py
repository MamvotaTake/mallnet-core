from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.schemas.subscription import (
    SubscriptionCreate,
    SubscriptionResponse,
)
from app.services.subscription_service import SubscriptionService
from app.repositories.subscription_repository import SubscriptionRepository

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])


@router.post("/", response_model=SubscriptionResponse)
def create_subscription_form(
    mall_id: int = Form(...),
    package_id: int = Form(...),
    mac_address: str = Form(...),
    db: Session = Depends(get_db),
):
    service = SubscriptionService(db)
    return service.create_subscription(
        mall_id=mall_id,
        package_id=package_id,
        mac_address=mac_address,
    )


@router.get("/", response_model=List[SubscriptionResponse])
def list_subscriptions(db: Session = Depends(get_db)):
    repo = SubscriptionRepository(db)
    return repo.get_all()
