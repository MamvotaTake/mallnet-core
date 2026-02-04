def export_voucher_cards(vouchers, mall_id, profile):
    path = f"exports/vouchers_mall_{mall_id}_{profile}.csv"

    with open(path, "w") as f:
        f.write("CODE,PIN,PROFILE\n")
        for v in vouchers:
            f.write(f"{v['code']},{v['pin']},{v['profile']}\n")

    return path
