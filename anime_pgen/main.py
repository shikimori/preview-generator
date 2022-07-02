import json
import os
import shutil
from pathlib import Path

import typer
import yaml

from typing import List, Tuple
from joblib import Parallel, delayed
from colour import Color

from anime_pgen import make
from anime_pgen.Item import Item
from anime_pgen.utils import eprint, pretty_print
from anime_pgen.constants import DEFAULT_SAVE_FILE, COLORS, SIZES, SIZE
from anime_pgen.download import download_many

app = typer.Typer()


@app.command('fetch')
def fetch(
        item_id: str or int = typer.Argument(..., help="Target anime/manga id(s)"),
        multiple: bool = typer.Option(False, '--multiple', '-M', help="Need to process multiple ids"),
        application_name: str = typer.Option(..., '--app-name', help="Application name for requests"),
        save_path: str = typer.Option(default=DEFAULT_SAVE_FILE, help="File to save list of targets"),
        is_manga: bool = typer.Option(False, '--manga', '-m', help="Download manga info"),
):
    """
    Fetch anime or manga and save to file
    """
    if multiple and ',' in item_id:
        item_ids: List[int] = [
            int(i.strip()) for i in item_id.split(',')
        ]
    elif item_id.isnumeric():
        item_ids = [int(item_id)]
    elif isinstance(item_id, int):
        item_ids = [item_id]
    else:
        if ',' in item_id and not multiple:
            eprint('Seems like you want to fetch many items. Use `--multiple` flag')
        else:
            eprint('Incorrect `item_id` argument')

        typer.Abort()
        return

    items = download_many(item_ids, application_name, is_manga)

    if len(items) == 0:
        eprint('There is no result')
        typer.Abort()

    with open(save_path, 'w', encoding='utf8') as output_file:
        json.dump(items, output_file, ensure_ascii=False)
        typer.secho(f'Successfully saved to {save_path}', fg=typer.colors.GREEN)


@app.command()
def make_preview(
        input_file: str = typer.Argument(..., help="File with prefetched anime/manga"),
        output_folder: str = typer.Option(..., help="Output folder"),
        config_file: str = typer.Option(..., '--config', help="Config file in YAML format (see: config.example.yaml)"),
        application_name: str = typer.Option(..., '--app-name', help="Application name for requests"),
        multithread: bool = typer.Option(False, '-P', help="Use multithreading"),
        n_jobs: int = typer.Option(-1, '--n_jobs', help="Number of threads is multithreading is enabled"),
        demo_mode: bool = typer.Option(False, '--demo', help="Make demo sequence")
):
    """
    Make preview based on input and config
    """
    items_path = Path(input_file)
    output_folder = Path(output_folder)
    config_path = Path(config_file)

    tmp_dir = Path.cwd() / '.tmp_preview'

    if tmp_dir.exists():
        shutil.rmtree(tmp_dir)

    tmp_dir.mkdir(parents=True, exist_ok=True)

    if not items_path.exists():
        print('Input file does not exist. Abort')
        return typer.Abort()
    elif not config_path.exists():
        print('Config does not exist. Abort')
        return typer.Abort()
    elif not output_folder.is_dir():
        print('Output path is not a directory. Abort')
        return typer.Abort()

    with open(items_path, 'r') as items_f:
        items = json.load(items_f)

    with open(config_path, 'r') as config_f:
        config = yaml.load(config_f, Loader=yaml.FullLoader)

    colors = config.get('colors')
    size = config.get('size')
    content = config.get('content')

    if content is None:
        eprint('"content" section is required in config file')
        return typer.Abort()

    if colors is None:
        colors = COLORS
        print('There is no "colors" section, fallback to defaults')
        pretty_print({'colors': colors})

    if size is None:
        size = SIZE
        print('There is no "size" section, fallback to defaults')
        pretty_print({'size': size})

    proportion: float = 1 if size == 'big' else 0.5
    size: Tuple[int, int] = SIZES[size]

    bg_color = Color(colors.get('background', COLORS['background']))
    text_color = Color(colors.get('text', COLORS['text']))
    year_color = Color(colors.get('year', COLORS['year']))

    rating_color = colors.get('rating', COLORS['rating'])
    active_star_color = Color(rating_color.get('active', COLORS['rating']['active']))
    star_color = Color(rating_color.get('regular', COLORS['rating']['regular']))

    bg_tile = Path(content['images']['background_tile'])
    star_path = Path(content['images']['star'])
    glyph_path = Path(content['images']['logo']['glyph'])
    logo_path = Path(content['images']['logo']['text'])

    text_font = content['fonts']['text']
    number_font = content['fonts']['bold_text']
    bold_text_font = content['fonts']['numbers']
    japan_font = content['fonts']['japanese']

    prepared_items: List[Item] = []

    for item in items:
        p_item = make.prep_data(item, tmp_dir, application_name)

        if p_item is not None:
            prepared_items.append(p_item)

    result: List[str] = []

    if multithread:
        typer.secho('Using multithreading', fg=typer.colors.CYAN)
        result = Parallel(n_jobs=n_jobs)(delayed(make.make_preview)(
            input_item=item,
            output_file=output_folder,
            size=size,
            bg_tile=bg_tile,
            star_path=star_path,
            japan_font=japan_font,
            number_font=number_font,
            text_font=text_font,
            bold_text_font=bold_text_font,
            logo_path=logo_path,
            glyph_path=glyph_path,
            proportion=proportion,
            bg_color=bg_color,
            text_color=text_color,
            year_color=year_color,
            active_star_color=active_star_color,
            star_color=star_color,
        ) for item in prepared_items)
    else:
        for item in prepared_items:
            res = make.make_preview(
                input_item=item,
                output_file=output_folder,
                size=size,
                bg_tile=bg_tile,
                star_path=star_path,
                japan_font=japan_font,
                number_font=number_font,
                text_font=text_font,
                bold_text_font=bold_text_font,
                logo_path=logo_path,
                glyph_path=glyph_path,
                proportion=proportion,
                bg_color=bg_color,
                text_color=text_color,
                year_color=year_color,
                active_star_color=active_star_color,
                star_color=star_color,
                demo_mode=demo_mode,
            )

            result.append(res)

    typer.secho('Successfully create previews:', fg=typer.colors.GREEN)
    for res in result:
        print(f'\t - {res}')

    shutil.rmtree(tmp_dir)
