import qrcode
import json

def generate_qr(order_data):
    data = json.dumps(order_data)

    img = qrcode.make(data)
    file_path = "order_qr.png"
    img.save(file_path)

    return file_path