from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.mikrotik.client import MikroTikClient
from app.mikrotik.vouchers import MikroTikVoucherService
from app.repositories.internet_package_repository import InternetPackageRepository
from app.repositories.router_repository import RouterRepository
from app.utils.bulk_qr import bulk_generate_qr
from app.utils.voucher_pdf import generate_voucher_pdf

router = APIRouter(prefix="/mikrotik-vouchers", tags=["MikroTik Vouchers"])


@router.post("/generate")
def generate_voucher(mall_id: int, package_id: int, db: Session = Depends(get_db)):
    package = InternetPackageRepository(db).get_by_id(package_id)
    router_cfg = RouterRepository(db).get_by_mall(mall_id)

    mikrotik = MikroTikClient(
        host=router_cfg.host,
        username=router_cfg.username,
        password=router_cfg.password,
        port=router_cfg.api_port,
    )
    api = mikrotik.connect()

    voucher_service = MikroTikVoucherService(api)

    uptime_map = {
        1: "1d",
        7: "1w",
        30: "30d",
    }

    voucher = voucher_service.create_voucher(
        profile=package.mikrotik_profile,
        limit_uptime=uptime_map[package.duration_days],
    )

    return voucher


@router.get("/")
def list_vouchers(mall_id: int, db: Session = Depends(get_db)):
    router_cfg = RouterRepository(db).get_by_mall(mall_id)

    mikrotik = MikroTikClient(
        host=router_cfg.host,
        username=router_cfg.username,
        password=router_cfg.password,
        port=router_cfg.api_port,
    )
    api = mikrotik.connect()

    return MikroTikVoucherService(api).list_vouchers()


@router.delete("/{code}")
def delete_voucher(mall_id: int, code: str, db: Session = Depends(get_db)):
    router_cfg = RouterRepository(db).get_by_mall(mall_id)

    mikrotik = MikroTikClient(
        host=router_cfg.host,
        username=router_cfg.username,
        password=router_cfg.password,
        port=router_cfg.api_port,
    )
    api = mikrotik.connect()

    ok = MikroTikVoucherService(api).delete_voucher(code)
    return {"deleted": ok}

@router.post("/bulk-generate-with-qr")
def bulk_generate_with_qr(
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

    qr_paths = bulk_generate_qr(mall_id, vouchers)

    return {
        "generated": len(vouchers),
        "profile": package.mikrotik_profile,
        "qr_folder": f"/static/vouchers/mall_{mall_id}/{package.mikrotik_profile}",
        "sample": vouchers[:3],
    }


@router.post("/bulk-generate-with-qr-pdf")
def bulk_generate_with_qr_pdf(
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

    # Generate QRs
    from app.utils.bulk_qr import bulk_generate_qr
    bulk_generate_qr(mall_id, vouchers)

    # Generate PDF
    pdf_path = generate_voucher_pdf(
        mall_id=mall_id,
        profile=package.mikrotik_profile,
        vouchers=vouchers,
    )

    return {
        "generated": len(vouchers),
        "profile": package.mikrotik_profile,
        "pdf": f"/{pdf_path}",
    }
