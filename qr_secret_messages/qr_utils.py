import io
from PIL import Image
import qrcode
from pyzbar import pyzbar


def generate_qr_code(data: bytes, size: int = 10, border: int = 4) -> Image.Image:
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=size,
        border=border,
    )
    qr.add_data(data.decode('utf-8'))
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img


def read_qr_code(image_path: str) -> bytes:
    try:
        image = Image.open(image_path)
        decoded_objects = pyzbar.decode(image)
        if not decoded_objects:
            raise ValueError("No QR code found in the image.")
        qr_data = decoded_objects[0].data
        if isinstance(qr_data, str):
            qr_data = qr_data.encode('utf-8')
        return qr_data
    except Exception as e:
        raise ValueError(f"Failed to read QR code: {str(e)}") from e


def save_qr_code(qr_image: Image.Image, filepath: str) -> None:
    qr_image.save(filepath, 'PNG')
