from io import BytesIO
from PIL import Image
from django.core.files import File


def compress(image, quality: int = 70):
    im = Image.open(image)
    im_io = BytesIO()
    im.save(im_io, im.format, quality=quality)
    new_image = File(im_io, name=image.name)
    return new_image
