import math

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from PIL.Image import Image as ImageType
from colour import Color

from typing import Tuple, Dict, List

from anime_pgen.Item import Item
from anime_pgen.utils import resize, invert, make_transparent, replace_color, fill_bg_with_tiles, bruteforce, \
    find_suitable_fontsize, add_corners, eprint


def prep_data(raw_data: Dict, tmp_dir: Path, application_name: str) -> Item or None:
    try:
        item = Item(raw_data)
        item.download(tmp_dir, application_name)

        return item
    except Exception as e:
        eprint(e)

    return None


def _get_two_part_logo_size(second_part: ImageType, first_part: ImageType):
    return first_part.width + 5 + second_part.width, max(second_part.height, first_part.height)


def _draw_two_part_logo(
        x: int, y: int,
        image: ImageType,
        second_part: ImageType, first_part: ImageType
) -> Tuple[int, int]:
    image.paste(first_part, (x, y), first_part)
    image.paste(second_part, (x + first_part.width + 5, y), second_part)

    return first_part.width + 5 + second_part.width, max(second_part.height, first_part.height)


def make_preview(input_item: Item,
                 output_file: Path,
                 size: Tuple[int, int],
                 bg_tile: str or Path,
                 star_path: str or Path,
                 japan_font: str or Path,
                 number_font: str or Path,
                 text_font: str or Path,
                 bold_text_font: str or Path,
                 logo_path: str or Path,
                 glyph_path: str or Path,
                 proportion: float,
                 bg_color: Color,
                 text_color: Color,
                 year_color: Color,
                 active_star_color: Color,
                 star_color: Color,
                 demo_mode: bool = False
                 ):
    padding = int(70 * proportion)
    bottom_padding = padding + int(30 * proportion)

    max_description_lines = 3

    tile_bg = Image.open(bg_tile)

    # region Logo
    shiki_logo = resize(
        invert(
            make_transparent(logo_path)
        ),
        0.15 * proportion
    )
    shiki_glyph = resize(
        invert(
            make_transparent(glyph_path)
        ),
        0.15 * proportion
    )

    star_image = make_transparent(star_path)

    score_font = ImageFont.truetype(number_font, size=int(44 * proportion))
    kind_text = ImageFont.truetype(bold_text_font, size=int(24 * proportion))

    example_text_height = score_font.getbbox('8.0')[3]

    star = resize(star_image, int(example_text_height / 2) / star_image.size[0])
    active_star = replace_color(star, Color('#000000'), active_star_color)
    star = replace_color(star, Color('#000000'), star_color)
    description_font = ImageFont.truetype(text_font, size=int(24 * proportion))

    demo = {
        'path': Path.cwd() / 'demo_seq',
        'step': 0
    }

    def demo_screen(image):
        step = demo['step']
        image.save(str(demo['path'] / f'{step:04d}.jpg'))
        return step + 1

    if demo_mode:
        demo['path'].mkdir(exist_ok=True)

    def make_stars(img: ImageType, score: float, position: Tuple[int, int]):
        stars_x, stars_y = position
        old_stars_x = stars_x
        gap = 3

        star_width, star_height = star.size

        p, half_star_position = math.modf(score)
        half_star = active_star.crop((0, 0, int(star_width * p), star_height))

        for i in range(5):
            if i == half_star_position:
                img.paste(
                    star,
                    (stars_x, stars_y),
                    star
                )
                img.paste(
                    half_star,
                    (stars_x, stars_y),
                    half_star
                )
            else:
                to_draw = active_star if int(score) > i else star

                img.paste(
                    to_draw,
                    (stars_x, stars_y),
                    star
                )

            stars_x = stars_x + star_width + gap

        stars_x = stars_x + star_width

        return stars_x - old_stars_x

    def process_image(item: Item):
        # region Prep

        _avatar = Image.open(item.image).convert('RGB')

        image = Image.new('RGB', size, (255, 255, 255))
        image_editable = ImageDraw.Draw(image)

        if demo_mode:
            demo['step'] = demo_screen(image)

        image_width, image_height = image.size

        image = fill_bg_with_tiles(image, tile_bg)

        if demo_mode:
            demo['step'] = demo_screen(image)

        image_editable.rounded_rectangle((padding, padding, image_width - padding, image_height - bottom_padding),
                                         fill=bg_color.hex, radius=7)

        if demo_mode:
            demo['step'] = demo_screen(image)

        shiki_width, shiki_height = _get_two_part_logo_size(shiki_logo, shiki_glyph)

        _draw_two_part_logo(
            image_width - shiki_width - padding,
            image_height - int(shiki_height / 2) - padding,
            image,
            shiki_logo, shiki_glyph
        )

        if demo_mode:
            demo['step'] = demo_screen(image)
        # endregion

        # region Avatar
        avatar_position = (padding, padding)
        avatar_width, avatar_height = _avatar.size

        max_avatar_height = image_height - padding - bottom_padding

        max_avatar_width = 350 * proportion

        if avatar_height < avatar_width:
            avatar_scale = max_avatar_width / avatar_width

            avatar = resize(_avatar, avatar_scale)
            avarar_mask = add_corners(avatar, 0)
            diff = (max_avatar_height - avatar.size[1]) / 2 + padding

            avatar_position = (padding, math.ceil(diff))
        else:
            avatar_scale = max_avatar_height / avatar_height

            avatar = resize(_avatar, avatar_scale)
            avarar_mask = add_corners(avatar, 7)

        avatar_width, avatar_height = avatar.size

        image.paste(avatar, avatar_position, avarar_mask)

        if demo_mode:
            demo['step'] = demo_screen(image)
        # endregion

        start_x = padding + avatar_width + padding
        start_y = padding + padding

        end_x = image_width - padding - padding
        end_y = image_height - bottom_padding - padding

        max_width = end_x - start_x
        image_editable.rounded_rectangle((padding, padding, image_width - padding, image_height - bottom_padding),
                                         radius=7, outline=star_color.hex,
                                         width=1)

        if demo_mode:
            demo['step'] = demo_screen(image)

        # region Header

        length = 40

        header = item.name
        header_text = None
        if header is not None and header != '':
            _header_font = ImageFont.truetype(bold_text_font, size=int(40 * proportion))

            there_is_year = False

            if item.aired_on is not None and item.year is not None:
                header = item.year + f'/{header}'
                there_is_year = True

            if len(header) > 60:
                header_font = find_suitable_fontsize(max_width, _header_font, header, length)
            else:
                header_font = _header_font

            header_text = bruteforce(header, max_width, header_font,
                                     count=length)
            header_line_height = header_font.getbbox(header_text[0])[3]

            pattern: List[Tuple[str, Tuple[int, int]]] = []
            for i in range(len(header_text)):
                text = header_text[i]

                if i == 0:
                    padding_y = 0
                else:
                    padding_y = i * header_line_height

                pattern.append((text, (0, padding_y)))

            if item.en:
                start_y = start_y - int(header_line_height / 3)
            else:
                start_y = start_y - int(header_line_height / 2.5)

            if there_is_year:
                year_font = ImageFont.truetype(text_font, size=header_font.size)
            else:
                year_font = None

            is_first = True

            for text, bounds in pattern:
                x, y = bounds

                if is_first and there_is_year:
                    is_first = False
                    year_width = year_font.getbbox(text[0:5])[2]
                    image_editable.text((start_x + x, start_y + y), text[0:5], year_color.hex, font=year_font)
                    image_editable.text((start_x + x + year_width, start_y + y), text[5:], text_color.hex,
                                        font=header_font)
                else:
                    image_editable.text((start_x + x, start_y + y), text, text_color.hex, font=header_font)

            start_y = start_y + pattern[-1][1][1] + header_line_height

        if demo_mode:
            demo['step'] = demo_screen(image)

        # endregion

        # region Subheader
        is_japanese = False

        if item.en:
            subheader = item.japanese
            is_japanese = True
        else:
            subheader = item.name_en

        if subheader is not None and subheader != '':
            _subheader_font = ImageFont.truetype(japan_font if is_japanese else text_font, size=int(24 * proportion))
            if _subheader_font.getbbox(subheader)[2] > max_width:
                subheader_font = find_suitable_fontsize(max_width, _subheader_font, subheader,
                                                        len(subheader))
            else:
                subheader_font = _subheader_font

            sx, sy, subheader_width, subheader_height = subheader_font.getbbox(subheader)

            subheader_y = int(start_y + subheader_height / 2)

            image_editable.text((start_x, subheader_y), subheader, text_color.hex,
                                font=subheader_font)

            line_y = subheader_y + subheader_height

            start_y = int(line_y + subheader_height / 3)

        if demo_mode:
            demo['step'] = demo_screen(image)

        # endregion

        score_text = item.score_text

        score_text_height = score_font.getbbox(score_text)[3]

        rating_width = make_stars(image, item.score / 2,
                                  (start_x, start_y + int(score_text_height / 2.5)))

        if demo_mode:
            demo['step'] = demo_screen(image)

        image_editable.text((start_x + rating_width, start_y), score_text, text_color.hex,
                            font=score_font)

        if demo_mode:
            demo['step'] = demo_screen(image)

        start_y = start_y + score_text_height

        kind = item.kind
        if item.kind is not None and item.kind != '' and header_text is not None and len(header_text) <= 3:
            image_editable.text((start_x, start_y), kind, text_color.hex,
                                font=kind_text)

        if demo_mode:
            demo['step'] = demo_screen(image)

        # region Description

        description = item.description

        if description is not None and description != '':
            description_text = bruteforce(description, max_width, description_font,
                                          count=60)
            description_line_height = description_font.getbbox(description_text[0])[3]

            pattern: List[Tuple[str, Tuple[int, int]]] = []

            description_array_length = min(len(description_text), max_description_lines)

            for i in range(description_array_length):
                text = description_text[i]

                if i == 0:
                    padding_y = 0
                else:
                    padding_y = i * description_line_height

                pattern.append((text, (0, padding_y)))

            if pattern[description_array_length - 1][1][1] + start_y < end_y:
                start_y = start_y + (end_y - (pattern[description_array_length - 1][1][1] + start_y))

            if description_array_length == max_description_lines and len(description_text) > max_description_lines:
                pattern[-1] = (pattern[-1][0] + '...', pattern[-1][1])

            for text, bounds in pattern:
                x, y = bounds
                image_editable.text((start_x + x, start_y + y), text, text_color.hex, font=description_font)

        if demo_mode:
            demo['step'] = demo_screen(image)

        # endregion

        filename = str(output_file / item.result_path)

        image.save(filename)

        return filename

    return process_image(input_item)
