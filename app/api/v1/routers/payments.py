from datetime import datetime
from urllib import request

from fastapi import APIRouter, Depends, HTTPException,Request
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repositories.internet_package_repository import InternetPackageRepository
from app.repositories.payment_repository import PaymentRepository
from app.schemas.payment import PaymentCreate, PaymentResponse
from app.services.ecocash_service import EcoCashService
from app.services.payment_service import PaymentService
from app.services.subscription_service import SubscriptionService
from app.utils.reference_parser import parse_reference

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("/", response_model=PaymentResponse)
def make_payment(
    payload: PaymentCreate,
    db: Session = Depends(get_db),
):
    service = PaymentService(db)
    try:
        result = service.process_payment(
            user_id=payload.user_id,
            package_id=payload.package_id,
            method=payload.method,
            reference=payload.reference,
        )
        return result["payment"]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/ecocash")
def pay_with_ecocash(payload: PaymentCreate, db: Session = Depends(get_db)):
    package = InternetPackageRepository(db).get_by_id(payload.package_id)

    payment = PaymentRepository(db).create(
        user_id=payload.user_id,
        package_id=payload.package_id,
        amount=package.price,
        method="ecocash",
        reference=f"QR-{payload.user_id}-{payload.package_id}",
    )

    ecocash = EcoCashService()
    response = ecocash.initiate_payment(
        reference=payment.reference,
        email="guest@mallnet.africa",
        phone=payload.phone,
        amount=payment.amount,
    )

    return {
        "message": "EcoCash payment initiated",
        "instructions": response["instructions"],
    }

@router.post("/payments/paynow-callback")
def paynow_callback(request: Request, db: Session = Depends(get_db)):
    status = request.form.get("status")
    reference = request.form.get("reference")
    amount = float(request.form.get("amount"))

    if status != "Paid":
        return "IGNORED"

    mall_id, package_id = parse_reference(reference)

    # Create or get user based on MAC or phone (simplified)
    user_id = get_or_create_guest_user(db, mall_id)

    # Record payment
    payment = PaymentRepository(db).create(
        user_id=user_id,
        package_id=package_id,
        amount=amount,
        method="ecocash",
        reference=reference,
    )

    # Activate subscription
    SubscriptionService(db).create_subscription(
        user_id=user_id,
        package_id=package_id,
    )

    return "OK"