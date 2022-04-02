import sys
from typing import Dict
from .image import add_corners, fill_bg_with_tiles, resize, replace_color, make_transparent, invert
from .text import bruteforce, find_suitable_fontsize


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def pretty_print(d: Dict, indent: int = 0):
    for key, value in d.items():
        print('\t' * indent + str(key))
        if isinstance(value, dict):
            pretty_print(value, indent + 1)
        else:
            print('\t' * (indent + 1) + str(value))
