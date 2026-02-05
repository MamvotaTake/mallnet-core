def export_voucher_cards(vouchers, mall_id, profile):
    path = f"exports/vouchers_mall_{mall_id}_{profile}.csv"

    with open(path, "w") as f:
        f.write("CODE,PIN,PROFILE\n")
        for v in vouchers:
            voucher_profile = v.get("profile") or v.get("mikrotik_profile")
            f.write(f"{v['code']},{v['pin']},{voucher_profile}\n")

    return path
