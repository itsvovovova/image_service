from PIL import Image, ImageOps
from io import BytesIO

def filter_photo(current_photo: bytes, current_filter: str) -> bytes:

    # Конвертируем байты в изображение
    image = Image.open(BytesIO(current_photo))

    match current_filter:
        case "rotate 45":
            result = image.rotate(45, expand=True)
        case "white-black":
            result = image.convert("L")
        case "negative":
            result = ImageOps.invert(image.convert("RGB"))
        case _:
            result = image

    byte_io = BytesIO()
    result.save(byte_io, format='PNG')
    rvalue = byte_io.getvalue()

    return rvalue

