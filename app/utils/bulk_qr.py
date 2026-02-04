from app.utils.qr import generate_voucher_qr


def bulk_generate_qr(mall_id: int, vouchers: list):
    paths = []

    for v in vouchers:
        path = generate_voucher_qr(
            mall_id=mall_id,
            profile=v["profile"],
            code=v["code"],
            pin=v["pin"],
        )
        paths.append(path)

    return paths
