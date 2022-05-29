import os
import pytest
import numpy as np
import shutil

from PIL import Image
from pathlib import Path 


def assert_images_equal(image_1: str, image_2: str):
    img1 = Image.open(image_1)
    img2 = Image.open(image_2)

    sum_sq_diff = np.sum((np.asarray(img1).astype('float') - np.asarray(img2).astype('float')) ** 2)

    if sum_sq_diff == 0:
        # Images are exactly the same
        pass
    else:
        normalized_sum_sq_diff = sum_sq_diff / np.sqrt(sum_sq_diff)
        assert normalized_sum_sq_diff < 0.001


@pytest.fixture
def image_similarity(request, tmpdir):
    testname = request.node.name
    filename = f"{testname}.jpg"
    generated_file = os.path.join(str(tmpdir), filename)

    yield {'filename': generated_file}

    target_file = Path().cwd() / 'tests' / 'baseline_images' / filename

    if not target_file.exists():
        shutil.copyfile(generated_file, target_file)
        pass

    assert_images_equal(str(target_file), generated_file)
