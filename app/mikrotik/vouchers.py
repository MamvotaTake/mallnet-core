import secrets
import time


class MikroTikVoucherService:
    def __init__(self, api):
        self.users = api.get_resource("/ip/hotspot/user")

    def _generate_code_pin(self):
        code = secrets.token_hex(3).upper()     # e.g A9F3D2
        pin = secrets.randbelow(9000) + 1000    # 4-digit PIN
        return code, str(pin)

    def create_voucher(self, profile: str, limit_uptime: str):
        code, pin = self._generate_code_pin()

        self.users.add(
            name=code,
            password=pin,
            profile=profile,
            limit_uptime=limit_uptime,
            disabled="no",
        )

        return {
            "code": code,
            "pin": pin,
            "profile": profile,
            "limit_uptime": limit_uptime,
        }

    def bulk_create(
        self,
        profile: str,
        limit_uptime: str,
        quantity: int,
        batch_size: int = 50,
    ):
        vouchers = []

        for i in range(quantity):
            vouchers.append(
                self.create_voucher(profile, limit_uptime)
            )

            # Throttle every batch
            if (i + 1) % batch_size == 0:
                time.sleep(0.5)

        return vouchers

    def list_vouchers(self):
        return self.users.get()

    def disable_voucher(self, code: str):
        users = self.users.get(name=code)
        if not users:
            return False

        self.users.set(
            id=users[0][".id"],
            disabled="yes",
        )
        return True

    def delete_voucher(self, code: str):
        users = self.users.get(name=code)
        if not users:
            return False

        self.users.remove(id=users[0][".id"])
        return True
