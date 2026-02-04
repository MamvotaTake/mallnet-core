from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.mikrotik.client import MikroTikClient
from app.mikrotik.vouchers import MikroTikVoucherService
from app.repositories.internet_package_repository import InternetPackageRepository
from app.repositories.router_repository import RouterRepository
from app.schemas.voucher import VoucherCreate, VoucherResponse
from app.repositories.voucher_repository import VoucherRepository

router = APIRouter(prefix="/vouchers", tags=["Vouchers"])


@router.post("/", response_model=VoucherResponse)
def create_voucher(payload: VoucherCreate, db: Session = Depends(get_db)):
    repo = VoucherRepository(db)
    return repo.create(
        mall_id=payload.mall_id,
        package_id=payload.package_id,
        expires_at=payload.expires_at,
    )


@router.get("/{code}", response_model=VoucherResponse)
def get_voucher(code: str, db: Session = Depends(get_db)):
    repo = VoucherRepository(db)
    voucher = repo.get_by_code(code)
    if not voucher:
        raise HTTPException(status_code=404, detail="Voucher not found")
    return voucher


@router.get("/mall/{mall_id}", response_model=List[VoucherResponse])
def list_vouchers(mall_id: int, db: Session = Depends(get_db)):
    repo = VoucherRepository(db)
    return repo.list_by_mall(mall_id)

@router.post("/bulk-generate")
def bulk_generate_vouchers(
    mall_id: int,
    package_id: int,
    quantity: int = 100,
    db: Session = Depends(get_db),
):
    package = InternetPackageRepository(db).get_by_id(package_id)
    router_cfg = RouterRepository(db).get_by_mall(mall_id)

    mikrotik = MikroTikClient(
        host=router_cfg.host,
        username=router_cfg.username,
        password=router_cfg.password,
        port=router_cfg.api_port,
    )
    api = mikrotik.connect()

    uptime_map = {
        1: "1d",
        7: "1w",
        30: "30d",
    }

    service = MikroTikVoucherService(api)

    vouchers = service.bulk_create(
        profile=package.mikrotik_profile,
        limit_uptime=uptime_map[package.duration_days],
        quantity=quantity,
    )

    return {
        "generated": len(vouchers),
        "profile": package.mikrotik_profile,
        "vouchers": vouchers,
    }