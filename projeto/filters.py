from PIL import Image, ImageFilter
from PIL.ImageFilter import (
   BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
   EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN
)
import io, base64


def apply_filter(og_img, filter_func):
    image = Image.open(io.BytesIO(og_img))
    filtered_image = filter_func(image)

    img_io = io.BytesIO()
    image_format = image.format  # Obtém o formato original da imagem
    filtered_image.save(img_io, format=image_format)  # Salva a imagem filtrada com o mesmo formato
    img_bytes = img_io.getvalue()
    data_img = base64.b64encode(img_bytes).decode('ascii')
    return data_img

def black_and_white_filter(image):
    black_and_white_image = image.convert("L")
    return black_and_white_image

def blur_filter(image):
    img_blur = image.filter(ImageFilter.BLUR)
    return img_blur