from PIL import Image
from io import BytesIO

def filter_photo(current_photo: bytes, current_filter: str) -> bytes:

    # Конвертируем байты в изображение
    image = Image.open(BytesIO(current_photo))

    from PIL import ImageFilter, ImageOps

    match current_filter:
        case "Negative":
            result = ImageOps.invert(image.convert("RGB"))
        case "Black & White":
            result = image.convert("L")
        case "Soft Blur":
            result = image.filter(ImageFilter.GaussianBlur(radius=2))
        case "Sharpen Details":
            result = image.filter(ImageFilter.SHARPEN)
        case "Sketch Outline":
            result = image.filter(ImageFilter.FIND_EDGES)
        case "Contour Drawing":
            result = image.filter(ImageFilter.CONTOUR)
        case "Emboss Effect":
            result = image.filter(ImageFilter.EMBOSS)
        case "Poster Style":
            result = ImageOps.posterize(image.convert("RGB"), bits=3)
        case "Photo Negative":
            result = ImageOps.solarize(image.convert("RGB"), threshold=128)
        case _:
            result = image
    byte_io = BytesIO()
    result.save(byte_io, format='PNG')
    rvalue = byte_io.getvalue()

    return rvalue

