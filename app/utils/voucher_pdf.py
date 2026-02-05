from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from datetime import datetime
import os
import hashlib

# ------------------------------------------------------------------
# HARD PATCH: ReportLab + Python 3.8 OpenSSL compatibility
# ------------------------------------------------------------------
import reportlab.pdfbase.pdfdoc as pdfdoc

_original_md5 = hashlib.md5

def _safe_md5(*args, **kwargs):
    kwargs.pop("usedforsecurity", None)
    return _original_md5(*args, **kwargs)

pdfdoc.md5 = _safe_md5
# ------------------------------------------------------------------


def generate_voucher_pdf(
    mall_id: int,
    profile: str,
    vouchers: list,
) -> str:
    """
    Generate printable A4 PDF vouchers (12 per page).
    Each voucher contains:
      - Centered QR
      - PLAN (bold)
      - CODE
      - PIN
      - Login URL
    """

    output_dir = "exports/pdfs"
    os.makedirs(output_dir, exist_ok=True)

    filename = (
        f"{output_dir}/mall_{mall_id}_{profile}_"
        f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    )

    c = canvas.Canvas(filename, pagesize=A4)
    page_width, page_height = A4

    # -------------------------------
    # GRID CONFIG (12 vouchers/page)
    # -------------------------------
    cols, rows = 3, 4
    card_width = page_width / cols
    card_height = page_height / rows

    col = row = 0

    for v in vouchers:
        # Card origin
        x = col * card_width
        y = page_height - (row + 1) * card_height

        qr_path = f"static/vouchers/mall_{mall_id}/{profile}/{v['code']}.png"
        if not os.path.exists(qr_path):
            continue

        # -------------------------------
        # CARD BORDER
        # -------------------------------
        c.rect(
            x + 8,
            y + 8,
            card_width - 16,
            card_height - 16
        )

        # -------------------------------
        # QR CODE (CENTERED)
        # -------------------------------
        qr_size = 42 * mm
        qr_x = x + (card_width - qr_size) / 2
        qr_y = y + card_height - qr_size - 22

        c.drawImage(
            ImageReader(qr_path),
            qr_x,
            qr_y,
            qr_size,
            qr_size,
            preserveAspectRatio=True,
            mask="auto",
        )

        # -------------------------------
        # TEXT BLOCK (SINGLE, CLEAN)
        # -------------------------------
        text_x = x + 20
        text_y = y + 70

        voucher_profile = v.get("profile") or v.get("mikrotik_profile")

        # PLAN (primary)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(text_x, text_y, f"PLAN: {voucher_profile}")

        # CODE
        c.setFont("Helvetica", 10)
        c.drawString(text_x, text_y - 16, f"CODE: {v['code']}")

        # PIN
        c.drawString(text_x, text_y - 30, f"PIN:  {v['pin']}")

        # Footer
        login_url = f"http://localhost/login?voucher={v['code']}"
        c.setFont("Helvetica", 8)
        c.drawString(text_x, text_y - 50, "Scan QR or visit:")
        c.drawString(text_x, text_y - 62, login_url)

        # -------------------------------
        # GRID MOVE
        # -------------------------------
        col += 1
        if col == cols:
            col = 0
            row += 1

        if row == rows:
            c.showPage()
            row = 0

    c.save()
    return filename
