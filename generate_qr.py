import qrcode
from PIL import Image, ImageDraw

# ========= CONFIG CƠ BẢN =========
URL = "https://tryhardzz.github.io/love_letter/"
OUT = "qr_code.png"
BACKGROUND_PATH = "img/background.png"   # ảnh nền có sẵn (PNG/JPG)

# QR params
VERSION = 3
EC = qrcode.constants.ERROR_CORRECT_H
CELL = 8
BORDER_CELLS = 4
HEART_COLOR = (255, 105, 180)  # hồng đậm

# ========= VỊ TRÍ & KÍCH CỠ TRONG ẢNH NỀN =========
scale_factor = 0.3
pos_mode = "custom"   # "center" hoặc "custom"
qr_x, qr_y = 650, 450 # toạ độ góc trái QR trong ảnh nền (nếu custom)

# ========= HỘP QUÀ CONFIG =========
BOX_PADDING_X = 5      # khoảng cách QR với viền hộp (trái/phải)
BOX_PADDING_Y = 5      # khoảng cách QR với viền hộp (trên/dưới)
LID_HEIGHT = 30         # chiều cao nắp hộp
RIBBON_SIZE = 40        # kích thước nơ
BOX_COLOR = "#ffc6d7"   # màu thân hộp
LID_COLOR = "#fcb8c5"   # màu nắp hộp
RIBBON_COLOR = "#e04b75"
OUTLINE_COLOR = "#f38ba0"

# ========= TẠO MÃ QR =========
qr = qrcode.QRCode(
    version=VERSION,
    error_correction=EC,
    box_size=1,
    border=BORDER_CELLS,
)
qr.add_data(URL)
qr.make(fit=True)
M = qr.get_matrix()
N = len(M)

# ========= NẠP ẢNH NỀN =========
bg = Image.open(BACKGROUND_PATH).convert("RGBA")
canvas_w, canvas_h = bg.size
draw = ImageDraw.Draw(bg)

# ========= TÍNH KÍCH CỠ QR =========
qr_px = int(min(canvas_w, canvas_h) * scale_factor)
CELL = qr_px // N
qr_px = N * CELL

if pos_mode == "center":
    qr_x = (canvas_w - qr_px) // 2
    qr_y = (canvas_h - qr_px) // 2

# ========= VẼ HỘP QUÀ =========
box_left = qr_x - BOX_PADDING_X - 10
box_right = qr_x + qr_px + BOX_PADDING_X + 10
box_top = qr_y - BOX_PADDING_Y
box_bottom = qr_y + qr_px + BOX_PADDING_Y

# Thân hộp
draw.rectangle(
    [box_left, box_top, box_right, box_bottom],
    fill=BOX_COLOR, outline=OUTLINE_COLOR, width=4
)

# Nắp hộp (ngang phần trên thân)
draw.rectangle(
    [box_left - 10, box_top - LID_HEIGHT, box_right + 10, box_top],
    fill=LID_COLOR, outline=OUTLINE_COLOR, width=3
)

# Nơ trên nắp
mid_x = (box_left + box_right) // 2
ribbon_center_y = box_top - LID_HEIGHT - 5
draw.polygon([
    (mid_x, ribbon_center_y),
    (mid_x - RIBBON_SIZE, ribbon_center_y - RIBBON_SIZE // 1.5),
    (mid_x - RIBBON_SIZE * 1.5, ribbon_center_y),
    (mid_x - RIBBON_SIZE, ribbon_center_y + RIBBON_SIZE // 1.5)
], fill=RIBBON_COLOR)

draw.polygon([
    (mid_x, ribbon_center_y),
    (mid_x + RIBBON_SIZE, ribbon_center_y - RIBBON_SIZE // 1.5),
    (mid_x + RIBBON_SIZE * 1.5, ribbon_center_y),
    (mid_x + RIBBON_SIZE, ribbon_center_y + RIBBON_SIZE // 1.5)
], fill=RIBBON_COLOR)

draw.ellipse(
    [mid_x - 12, ribbon_center_y - 12, mid_x + 12, ribbon_center_y + 12],
    fill="#d63863"
)

# ========= VẼ QR CODE DẠNG TRÁI TIM =========
for y, row in enumerate(M):
    for x, val in enumerate(row):
        if not val:
            continue
        cx = qr_x + x * CELL + CELL // 2
        cy = qr_y + y * CELL + CELL // 2
        r = int(CELL / 2.1)
        heart = [
            (cx, cy + r),
            (cx - r, cy),
            (cx - r, cy - r),
            (cx, cy - r // 2),
            (cx + r, cy - r),
            (cx + r, cy),
            (cx, cy + r),
        ]
        draw.polygon(heart, fill=HEART_COLOR)

# ========= LƯU =========
bg.save(OUT)
print(f"✅ Saved: {OUT}")
print(f"📐 Image size: {canvas_w}×{canvas_h}, QR {qr_px}px at ({qr_x},{qr_y})")
