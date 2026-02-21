import re


MAC_REGEX = re.compile(r"^[0-9A-F]{2}(:[0-9A-F]{2}){5}$", re.I)


class HotspotService:
    def __init__(self, api):
        self.users = api.get_resource("/ip/hotspot/user")

    # -------------------------
    # Voucher helpers
    # -------------------------
    def list_voucher_users(self):
        users = self.users.get()
        vouchers = []

        for user in users:
            name = user.get("name", "")
            if not MAC_REGEX.match(name):
                vouchers.append(user)

        return vouchers

    def delete_voucher_user(self, voucher_code: str):
        users = self.users.get(name=voucher_code)
        if not users:
            return False

        self.users.remove(id=users[0][".id"])
        return True

    def delete_all_vouchers(self):
        vouchers = self.list_voucher_users()
        for user in vouchers:
            self.users.remove(id=user[".id"])

        return len(vouchers)

    # -------------------------
    # MAC-based users (already existing)
    # -------------------------
    def create_mac_user(self, mac_address: str, profile: str):
        self.create_or_update_mac_user(
            mac_address=mac_address,
            profile=profile,
            disabled=False,
        )

    def create_or_update_mac_user(
            self,
            mac_address: str,
            profile: str,
            disabled: bool = False,
    ):
        """
        Idempotent MAC user handler:
        - If MAC exists → update profile / disabled
        - If MAC does not exist → create it
        """

        users = self.users.get(name=mac_address)

        if users:
            user = users[0]
            user_id = user.get(".id") or user.get("id")

            if not user_id:
                return

            self.users.set(
                id=user_id,
                profile=profile,
                disabled="yes" if disabled else "no",
            )
            return

        # Create new MAC-based hotspot user
        self.users.add(
            name=mac_address,
            mac_address=mac_address,
            profile=profile,
            disabled="yes" if disabled else "no",
        )
    def disable_mac_user(self, mac_address: str):
        users = self.users.get(name=mac_address)
        if not users:
            return

        user = users[0]
        user_id = user.get(".id") or user.get("id")

        if not user_id:
            return  # fail silently, do not crash backend

        self.users.set(
            id=user_id,
            disabled="yes",
        )
