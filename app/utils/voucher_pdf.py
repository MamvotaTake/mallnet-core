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

    output_dir = "exports/pdfs"
    os.makedirs(output_dir, exist_ok=True)

    filename = os.path.abspath(
        f"{output_dir}/mall_{mall_id}_{profile}_"
        f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    )

    c = canvas.Canvas(filename, pagesize=A4)
    page_width, page_height = A4

    # -------------------------------
    # PAGE + GRID CONFIG
    # -------------------------------
    top_margin = -20 * mm          # 🔼 PAGE TOP MARGIN
    cols, rows = 3, 4
    usable_height = page_height - top_margin
    card_width = page_width / cols
    card_height = usable_height / rows

    pad = 10 * mm
    qr_size = 40 * mm

    col = row = 0

    for v in vouchers:
        x = col * card_width
        y = usable_height - (row + 1) * card_height

        qr_path = os.path.abspath(
            f"static/vouchers/mall_{mall_id}/{profile}/{v['code']}.png"
        )
        if not os.path.exists(qr_path):
            continue

        # Shift everything down by top margin
        y += top_margin

        # -------------------------------
        # CARD BORDER
        # -------------------------------
        c.setLineWidth(0.8)
        c.roundRect(
            x + pad,
            y + pad,
            card_width - 2 * pad,
            card_height - 2 * pad,
            6,
        )

        # -------------------------------
        # QR CODE (CENTERED, TOP AREA)
        # -------------------------------
        qr_x = x + (card_width - qr_size) / 2
        qr_y = y + card_height - pad - qr_size - 8 * mm

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
        # FOOTER (BOTTOM OF CARD)
        # -------------------------------
        footer_y = y + pad + 6 * mm   # 🔽 BOTTOM-ALIGNED

        c.setFont("Helvetica", 8)
        c.drawCentredString(
            x + card_width / 2,
            footer_y + 10,
            "Scan QR to connect"
        )

        login_url = f"http://localhost/login?voucher={v['code']}"
        c.setFont("Helvetica", 7)
        c.drawCentredString(
            x + card_width / 2,
            footer_y,
            login_url
        )

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

    c.showPage()
    c.save()

    return filename