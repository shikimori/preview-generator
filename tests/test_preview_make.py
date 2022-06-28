import re
import shutil

import pytest  # noqa
import json
from pathlib import Path

from typer.testing import CliRunner

from preview_generator.main import app

runner = CliRunner()

base_dir = Path().cwd() / 'tests'
mocks_dir = base_dir / 'mocks'
tmp_dir = base_dir / 'tmp'

anime_test_table = ["1-cowboy-bebop", "5-cowboy-bebop-tengoku-no-tobira", "6-trigun", "7-witch-hunter-robin",
                    "8-bouken-ou-beet", "z15-eyeshield-21", "16-hachimitsu-to-clover", "17-hungry-heart-wild-striker",
                    "z18-initial-d-fourth-stage", "19-monster", "z20-naruto", "21-one-piece", "22-tennis-no-ouji-sama",
                    "23-ring-ni-kakero-1", "24-school-rumble", "25-sunabouzu", "z26-texhnolyze", "27-trinity-blood",
                    "z28-yakitate-japan", "29-zipang", "30-neon-genesis-evangelion",
                    "31-neon-genesis-evangelion-death-rebirth", "32-neon-genesis-evangelion-the-end-of-evangelion",
                    "33-kenpuu-denki-berserk", "43-koukaku-kidoutai",
                    "z44-rurouni-kenshin-meiji-kenkaku-romantan-tsuioku-hen",
                    "z45-rurouni-kenshin-meiji-kenkaku-romantan",
                    "46-rurouni-kenshin-meiji-kenkaku-romantan-ishinshishi-e-no-chinkonka", "47-akira", "48-hack-sign"]

manga_test_table = ["12138-don-dracula", "16-love-hina", "z21-death-note", "31-lovely-complex", "11396-aza",
                    "11402-open-sesame", "3150-captain-tsubasa-world-youth-tokubetsu-hen-saikyou-no-teki-holland-youth",
                    "46-kannade", "48-pretty-face", "52-whistle", "12166-nippon-mukashibanashi", "587-lucky-star",
                    "16857-qing-you-du-zhong", "11412-ranman", "11996-anonymous", "8-full-moon-wo-sagashite",
                    "1254-mai-otome-arashi", "60-", "62-junkie", "64-13-nichi-wa-kinyoubi", "67-2001-ya-monogatari",
                    "11422-orange-bubble-gum", "49641-ghost-walker", "123-tenshi-no-su", "4-yokohama-kaidashi-kikou",
                    "8-full-moon-wo-sagashite", "9-tsubasa-reservoir-chronicle", "124-aqua",
                    "20414-yamigarishi-kimaira-tenryuuhen", "z12-bleach"]


def get_anime():
    for i in range(len(anime_test_table)):
        item = anime_test_table[i]

        yield item


def get_manga():
    for i in range(len(manga_test_table)):
        item = manga_test_table[i]

        yield item


def setup_module(module):
    # Setup files for "30_animes" and "30_mangas" tests

    with open(mocks_dir / 'anime' / '30_animes' / 'source.json', 'r') as animes_file:
        animes = json.load(animes_file)

    with open(mocks_dir / 'manga' / '30_mangas' / 'source.json', 'r') as mangas_file:
        mangas = json.load(mangas_file)

    anime_prefix = tmp_dir / '30_animes'
    anime_prefix.mkdir(exist_ok=True)

    manga_prefix = tmp_dir / '30_mangas'
    manga_prefix.mkdir(exist_ok=True)

    for anime in animes:
        name = anime.get('url', '').replace('/animes/', '')

        with open(anime_prefix / f'{name}.pgen.json', 'w', encoding='utf8') as f:
            json.dump([anime], f, ensure_ascii=False)

    for manga in mangas:
        name = manga.get('url', '').replace('/mangas/', '')

        with open(manga_prefix / f'{name}.pgen.json', 'w', encoding='utf8') as f:
            json.dump([manga], f, ensure_ascii=False)


def teardown_module(module):
    shutil.rmtree(tmp_dir / '30_animes')
    shutil.rmtree(tmp_dir / '30_mangas')
    print('cleanup')


def test_manga_monster(image_similarity):
    config_file = mocks_dir / 'manga' / 'monster' / 'config.yaml'
    input_file = mocks_dir / 'manga' / 'monster' / '.pgen.json'
    output_folder = tmp_dir / 'monster'

    output_folder.mkdir(exist_ok=True)

    result = runner.invoke(app, [
        'make-preview', str(input_file),
        '--output-folder', str(output_folder),
        '--config', str(config_file),
        '--app-name', 'Anime.News'
    ])

    assert result.exit_code == 0
    assert 'Successfully create previews' in result.stdout

    fname = image_similarity['filename']

    shutil.copyfile(output_folder / '1.jpg', fname)


def test_anime_cowboy_beebop(image_similarity):
    config_file = mocks_dir / 'anime' / 'cowboy_beebop' / 'config.yaml'
    input_file = mocks_dir / 'anime' / 'cowboy_beebop' / '.pgen.json'
    output_folder = tmp_dir / 'cowboy_beebop'

    output_folder.mkdir(exist_ok=True)

    result = runner.invoke(app, [
        'make-preview', str(input_file),
        '--output-folder', str(output_folder),
        '--config', str(config_file),
        '--app-name', 'Anime.News'
    ])

    assert result.exit_code == 0
    assert 'Successfully create previews' in result.stdout

    fname = image_similarity['filename']

    shutil.copyfile(output_folder / '1.jpg', fname)


@pytest.mark.parametrize('anime', get_anime())
def test_anime_using_table(anime, image_similarity):
    config_file = mocks_dir / 'anime' / '30_animes' / 'config.yaml'
    input_file = tmp_dir / '30_animes' / f'{anime}.pgen.json'
    output_folder = tmp_dir / '30_animes' / f'{anime}'

    output_folder.mkdir(exist_ok=True)

    result = runner.invoke(app, [
        'make-preview', str(input_file),
        '--output-folder', str(output_folder),
        '--config', str(config_file),
        '--app-name', 'Anime.News'
    ])

    assert result.exit_code == 0
    assert 'Successfully create previews' in result.stdout

    fname = image_similarity['filename']

    anime_id = re.sub(r'-.*?$', '', anime)
    anime_id = re.sub(r'\D', '', anime_id)

    shutil.copyfile(output_folder / f'{anime_id}.jpg', fname)


@pytest.mark.parametrize('manga', get_manga())
def test_manga_using_table(manga, image_similarity):
    config_file = mocks_dir / 'manga' / '30_mangas' / 'config.yaml'
    input_file = tmp_dir / '30_mangas' / f'{manga}.pgen.json'
    output_folder = tmp_dir / '30_mangas' / f'{manga}'

    output_folder.mkdir(exist_ok=True)

    result = runner.invoke(app, [
        'make-preview', str(input_file),
        '--output-folder', str(output_folder),
        '--config', str(config_file),
        '--app-name', 'Anime.News'
    ])

    assert result.exit_code == 0
    assert 'Successfully create previews' in result.stdout

    fname = image_similarity['filename']

    manga_id = re.sub(r'-.*?$', '', manga)
    manga_id = re.sub(r'\D', '', manga_id)

    shutil.copyfile(output_folder / f'{manga_id}.jpg', fname)
