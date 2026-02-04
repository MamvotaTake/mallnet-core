import qrcode
import os
from PIL import Image, ImageDraw, ImageFont


def generate_voucher_qr(
    mall_id: int,
    profile: str,
    code: str,
    pin: str,
):
    base_url = "http://127.0.0.1:8000/login"
    qr_url = f"{base_url}?username={code}&password={pin}"

    # Generate QR
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_url)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    # Add text area below QR
    width, height = qr_img.size
    extra_height = 120
    new_img = Image.new("RGB", (width, height + extra_height), "white")
    new_img.paste(qr_img, (0, 0))

    draw = ImageDraw.Draw(new_img)

    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 22)
    except:
        font = ImageFont.load_default()

    text_y = height + 10
    draw.text((20, text_y),     f"CODE: {code}", fill="black", font=font)
    draw.text((20, text_y+35),  f"PIN:  {pin}", fill="black", font=font)
    draw.text((20, text_y+70),  f"PLAN: {profile}", fill="black", font=font)

    # Save
    folder = f"static/vouchers/mall_{mall_id}/{profile}"
    os.makedirs(folder, exist_ok=True)

    path = f"{folder}/{code}.png"
    new_img.save(path)

    return path
