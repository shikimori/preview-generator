import shutil

import pytest  # noqa
from pathlib import Path

from typer.testing import CliRunner

from preview_generator.main import app

runner = CliRunner()

base_dir = Path().cwd() / 'tests'
mocks_dir = base_dir / 'mocks'
tmp_dir = base_dir / 'tmp'


def test_manga_monster(image_similarity):
    config_file = mocks_dir / 'monster' / 'config.yaml'
    input_file = mocks_dir / 'monster' / '.pgen.json'
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
