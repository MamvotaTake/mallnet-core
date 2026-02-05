from typing import Dict, List

from fastapi import HTTPException

from app.mikrotik.client import MikroTikClient
from app.mikrotik.vouchers import MikroTikVoucherService
from app.repositories.internet_package_repository import InternetPackageRepository
from app.repositories.router_repository import RouterRepository
from app.utils.bulk_qr import bulk_generate_qr
from app.utils.voucher_pdf import generate_voucher_pdf


class MikrotikVoucherService:
    def __init__(self, db):
        self.db = db
        self.package_repo = InternetPackageRepository(db)
        self.router_repo = RouterRepository(db)

    def _get_router(self, mall_id: int):
        router = self.router_repo.get_by_mall(mall_id)
        if not router:
            raise HTTPException(status_code=404, detail="Router not configured")
        return router

    def _get_package(self, package_id: int):
        package = self.package_repo.get_by_id(package_id)
        if not package:
            raise HTTPException(status_code=404, detail="Internet package not found")
        return package

    def _uptime_map(self, duration_days: int) -> str:
        mapping = {
            1: "1d",
            7: "1w",
            30: "30d",
        }
        if duration_days not in mapping:
            raise HTTPException(
                status_code=400,
                detail="Unsupported package duration",
            )
        return mapping[duration_days]

    def _api(self, mall_id: int):
        router = self._get_router(mall_id)
        client = MikroTikClient(
            host=router.host,
            username=router.username,
            password=router.password,
            port=router.api_port,
        )
        try:
            return client.connect()
        except Exception as exc:
            raise HTTPException(
                status_code=502,
                detail="Unable to connect to MikroTik API",
            ) from exc

    def generate_voucher(self, mall_id: int, package_id: int) -> Dict:
        package = self._get_package(package_id)
        try:
            api = self._api(mall_id)
            service = MikroTikVoucherService(api)
            limit_uptime = self._uptime_map(package.duration_days)
            return service.create_voucher(
                profile=package.mikrotik_profile,
                limit_uptime=limit_uptime,
            )
        except Exception as exc:
            raise HTTPException(
                status_code=502,
                detail="Failed to create MikroTik voucher",
            ) from exc

    def list_vouchers(self, mall_id: int) -> List[Dict]:
        try:
            api = self._api(mall_id)
            return MikroTikVoucherService(api).list_vouchers()
        except Exception as exc:
            raise HTTPException(
                status_code=502,
                detail="Failed to list MikroTik vouchers",
            ) from exc

    def delete_voucher(self, mall_id: int, code: str) -> Dict:
        try:
            api = self._api(mall_id)
            ok = MikroTikVoucherService(api).delete_voucher(code)
            return {"deleted": ok}
        except Exception as exc:
            raise HTTPException(
                status_code=502,
                detail="Failed to delete MikroTik voucher",
            ) from exc

    def bulk_generate_with_qr(
        self,
        mall_id: int,
        package_id: int,
        quantity: int,
    ) -> Dict:
        package = self._get_package(package_id)
        if quantity <= 0:
            raise HTTPException(status_code=400, detail="Quantity must be positive")
        try:
            api = self._api(mall_id)
            limit_uptime = self._uptime_map(package.duration_days)
            service = MikroTikVoucherService(api)
            vouchers = service.bulk_create(
                profile=package.mikrotik_profile,
                limit_uptime=limit_uptime,
                quantity=quantity,
            )
            bulk_generate_qr(mall_id, vouchers)
            return {
                "generated": len(vouchers),
                "profile": package.mikrotik_profile,
                "qr_folder": f"/static/vouchers/mall_{mall_id}/{package.mikrotik_profile}",
                "sample": vouchers[:3],
            }
        except Exception as exc:
            raise HTTPException(
                status_code=502,
                detail="Failed to generate MikroTik vouchers",
            ) from exc

    def bulk_generate_with_qr_pdf(
        self,
        mall_id: int,
        package_id: int,
        quantity: int,
    ) -> Dict:
        package = self._get_package(package_id)
        if quantity <= 0:
            raise HTTPException(status_code=400, detail="Quantity must be positive")
        try:
            api = self._api(mall_id)
            limit_uptime = self._uptime_map(package.duration_days)
            service = MikroTikVoucherService(api)
            vouchers = service.bulk_create(
                profile=package.mikrotik_profile,
                limit_uptime=limit_uptime,
                quantity=quantity,
            )

            bulk_generate_qr(mall_id, vouchers)
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
        except Exception as exc:
            raise HTTPException(
                status_code=502,
                detail="Failed to generate MikroTik vouchers",
            ) from exc
