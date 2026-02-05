from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.services.mikrotik_voucher_service import MikrotikVoucherService

router = APIRouter(prefix="/mikrotik-vouchers", tags=["MikroTik Vouchers"])


@router.post("/generate")
def generate_voucher(mall_id: int, package_id: int, db: Session = Depends(get_db)):
    service = MikrotikVoucherService(db)
    return service.generate_voucher(mall_id=mall_id, package_id=package_id)


@router.get("/")
def list_vouchers(mall_id: int, db: Session = Depends(get_db)):
    service = MikrotikVoucherService(db)
    return service.list_vouchers(mall_id=mall_id)


@router.delete("/{code}")
def delete_voucher(mall_id: int, code: str, db: Session = Depends(get_db)):
    service = MikrotikVoucherService(db)
    return service.delete_voucher(mall_id=mall_id, code=code)

@router.post("/bulk-generate-with-qr")
def bulk_generate_with_qr(
    mall_id: int,
    package_id: int,
    quantity: int = 100,
    db: Session = Depends(get_db),
):
    service = MikrotikVoucherService(db)
    return service.bulk_generate_with_qr(
        mall_id=mall_id,
        package_id=package_id,
        quantity=quantity,
    )


@router.post("/bulk-generate-with-qr-pdf")
def bulk_generate_with_qr_pdf(
    mall_id: int,
    package_id: int,
    quantity: int = 100,
    db: Session = Depends(get_db),
):
    service = MikrotikVoucherService(db)
    return service.bulk_generate_with_qr_pdf(
        mall_id=mall_id,
        package_id=package_id,
        quantity=quantity,
    )
