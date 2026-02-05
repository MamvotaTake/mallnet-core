from app.utils.qr import generate_voucher_qr


def bulk_generate_qr(mall_id: int, vouchers: list):
    paths = []

    for v in vouchers:
        profile = v.get("profile") or v.get("mikrotik_profile")
        path = generate_voucher_qr(
            mall_id=mall_id,
            profile=profile,
            code=v["code"],
            pin=v["pin"],
        )
        paths.append(path)

    return paths
