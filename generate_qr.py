import qrcode

# Link đến web local hoặc online (nếu deploy sau này)
url = "http://localhost:5500/love_letter.html"

# Tạo QR
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,
)
qr.add_data(url)
qr.make(fit=True)

# Xuất ảnh QR
img = qr.make_image(fill_color="pink", back_color="white")
img.save("love_qr.png")
print("✅ QR code saved as love_qr.png")


# Cài pip install qrcode[pil], rồi chạy:
# python generate_qr.py