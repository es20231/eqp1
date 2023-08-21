from PIL import Image, ImageFilter
from PIL.ImageFilter import (
   BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
   EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN
)
import io

def black_and_white(og_img):
    image = Image.open(io.BytesIO(og_img))
    black_and_white_image = image.convert("L")
    
    # Salva a imagem em preto e branco como bytes no formato JPEG
    img_io = io.BytesIO()
    black_and_white_image.save(img_io, format='JPEG')
    img_bytes = img_io.getvalue()

    return img_bytes

def blur_filter(og_img):
    image = Image.open(io.BytesIO(og_img))
    img_blur = image.filter(BLUR)

    img_io = io.BytesIO()
    img_blur.save(img_io, format='JPEG')
    img_bytes = img_io.getvalue()

    return img_bytes


def sharpen_filter(og_img):
    image = Image.open(io.BytesIO(og_img))
    img_sharpen = image.filter(SHARPEN)

    img_io = io.BytesIO()
    img_sharpen.save(img_io, format='JPEG')
    img_bytes = img_io.getvalue()

    return img_bytes


def smooth_filter(og_img):
    image = Image.open(io.BytesIO(og_img))
    img_smooth = image.filter(SMOOTH)

    img_io = io.BytesIO()
    img_smooth.save(img_io, format='JPEG')
    img_bytes = img_io.getvalue()

    return img_bytes





    



    

