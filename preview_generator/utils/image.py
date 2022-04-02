import math

import numpy as np

from pathlib import Path

from PIL import Image, ImageDraw, ImageOps
from PIL.Image import Image as ImageType
from colour import Color


def make_transparent(p: str or Path) -> ImageType:
    image = Image.open(p).convert("RGBA")

    if image.mode in ('RGBA', 'LA') or (image.mode == 'P' and 'transparency' in image.info):
        alpha = image.convert('RGBA').split()[-1]
        image.putalpha(alpha)

    return image


def invert(image):
    if image.mode == 'RGBA':
        r, g, b, a = image.split()
        rgb_image = Image.merge('RGB', (r, g, b))

        inverted_image = ImageOps.invert(rgb_image)

        r2, g2, b2 = inverted_image.split()

        final_transparent_image = Image.merge('RGBA', (r2, g2, b2, a))

        return final_transparent_image
    else:
        inverted_image = ImageOps.invert(image)
        return inverted_image


def resize(img: ImageType, scale: float) -> ImageType:
    width, height = img.size

    return img.resize(
        (
            int(math.ceil(width * scale)),
            int(math.ceil(height * scale))
        )
    )


def fill_bg_with_tiles(img: ImageType, tile: ImageType):
    image_width, image_height = img.size
    tile_width, tile_height = tile.size

    for i in range(0, image_width, tile_width):
        for j in range(0, image_height, tile_height):
            img.paste(tile, (i, j), tile)

    return img


def replace_color(img: ImageType, before_color: Color, after_color: Color):
    img = img.convert('RGBA')

    data = np.array(img)
    red, green, blue, alpha = data.T

    white_areas = (red == before_color.red * 256) & (blue == before_color.blue * 256) & (
            green == before_color.green * 256)
    data[..., :-1][white_areas.T] = (
        after_color.red * 256, after_color.green * 256, after_color.blue * 256)  # Transpose back needed

    return Image.fromarray(data)


def add_corners(source: ImageType, rad):
    im = Image.new('RGBA', source.size)
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
    alpha = Image.new('L', im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    im.putalpha(alpha)
    return im
