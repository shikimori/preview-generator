import textwrap
from PIL import ImageFont


def bruteforce(text, max_width, font, count=40):
    lines = textwrap.wrap(text, width=count)

    final_text = []

    for line in lines:
        x, y, width, height = font.getbbox(line)

        if width >= max_width:
            return bruteforce(text, max_width, font, count - 10)
        else:
            final_text.append(line)

    return final_text


def find_suitable_fontsize(max_width: int, font: ImageFont, text: str, max_letters: int = 40) -> ImageFont:
    fontsize = 1
    font = ImageFont.truetype(font.path, fontsize)

    while font.getbbox(text[0:max_letters])[2] < max_width:
        # iterate until the text size is just larger than the criteria
        fontsize += 1
        font = ImageFont.truetype(font.path, fontsize)

    # optionally de-increment to be sure it is less than criteria
    fontsize -= 1
    return ImageFont.truetype(font.path, fontsize)
