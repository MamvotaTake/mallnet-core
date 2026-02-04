from app.mikrotik.client import MikroTikClient
from app.mikrotik.hotspot import HotspotService
from app.models.router import Router


class MikroTikVoucherService:
    def __init__(self, router: Router):
        self.client = MikroTikClient(
            host=router.host,
            username=router.username,
            password=router.password,
            port=router.api_port,
        )

    def list_vouchers(self):
        api = self.client.connect()
        hotspot = HotspotService(api)
        return hotspot.list_voucher_users()

    def delete_voucher(self, code: str):
        api = self.client.connect()
        hotspot = HotspotService(api)
        return hotspot.delete_voucher_user(code)

    def delete_all_vouchers(self):
        api = self.client.connect()
        hotspot = HotspotService(api)
        return hotspot.delete_all_vouchers()
