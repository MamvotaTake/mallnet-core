from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.schemas.voucher import VoucherCreate, VoucherResponse, VoucherRedeem
from app.schemas.subscription import SubscriptionResponse
from app.services.voucher_service import VoucherService

router = APIRouter(prefix="/vouchers", tags=["Vouchers"])


@router.post("/", response_model=VoucherResponse)
def create_voucher(payload: VoucherCreate, db: Session = Depends(get_db)):
    service = VoucherService(db)
    return service.create_voucher(
        mall_id=payload.mall_id,
        package_id=payload.package_id,
        expires_at=payload.expires_at,
    )


@router.get("/mall/{mall_id}", response_model=List[VoucherResponse])
def list_vouchers(mall_id: int, db: Session = Depends(get_db)):
    service = VoucherService(db)
    return service.list_by_mall(mall_id)


@router.get("/{code}", response_model=VoucherResponse)
def get_voucher(code: str, db: Session = Depends(get_db)):
    service = VoucherService(db)
    return service.get_voucher(code)

@router.post("/bulk-generate")
def bulk_generate_vouchers(
    mall_id: int,
    package_id: int,
    quantity: int = 100,
    db: Session = Depends(get_db),
):
    service = VoucherService(db)
    vouchers = service.bulk_generate(
        mall_id=mall_id,
        package_id=package_id,
        quantity=quantity,
    )

    return {
        "generated": len(vouchers),
        "vouchers": vouchers,
    }


@router.post("/redeem", response_model=SubscriptionResponse)
def redeem_voucher(payload: VoucherRedeem, db: Session = Depends(get_db)):
    service = VoucherService(db)
    return service.redeem_voucher(
        mall_id=payload.mall_id,
        mac_address=payload.mac_address,
        code=payload.code,
        pin=payload.pin,
    )
