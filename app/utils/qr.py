import qrcode
import os
from PIL import Image, ImageDraw, ImageFont


def generate_voucher_qr(mall_id, profile, code, pin):
    base_url = "http://localhost/login"
    qr_url = f"{base_url}?voucher={code}"

    # --- Generate QR ---
    qr = qrcode.QRCode(
        version=1,
        box_size=8,
        border=3,
    )
    qr.add_data(qr_url)
    qr.make(fit=True)

    qr_img = qr.make_image(
        fill_color="black",
        back_color="white"
    ).convert("RGB")

    qr_w, qr_h = qr_img.size

    # --- Canvas ---
    width = qr_w + 40
    height = qr_h + 160
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)

    # Center QR
    img.paste(qr_img, ((width - qr_w) // 2, 15))

    # --- Fonts ---
    try:
        plan_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 24)
        text_font = ImageFont.truetype("DejaVuSans.ttf", 20)
    except:
        plan_font = text_font = ImageFont.load_default()

    y = qr_h + 35

    # PLAN (ONCE)
    draw.text(
        (width // 2, y),
        f"PLAN: {profile.upper()}",
        fill="black",
        font=plan_font,
        anchor="mm"
    )
    y += 35

    # CODE
    draw.text(
        (width // 2, y),
        f"CODE: {code}",
        fill="black",
        font=text_font,
        anchor="mm"
    )
    y += 28

    # PIN
    draw.text(
        (width // 2, y),
        f"PIN: {pin}",
        fill="black",
        font=text_font,
        anchor="mm"
    )

    # --- Save ---
    folder = f"static/vouchers/mall_{mall_id}/{profile}"
    os.makedirs(folder, exist_ok=True)
    path = f"{folder}/{code}.png"

    img.save(path, dpi=(300, 300))
    return path