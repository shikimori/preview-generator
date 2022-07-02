import sys
import random
import time

from typing import List

import requests
from ratelimiter import RateLimiter

from anime_pgen.constants import GET_ANIME, GET_MANGA, ENDPOINT


@RateLimiter(max_calls=80, period=60)
def download_single(item_id: int, application_name: str, is_manga: bool = False):
    param = GET_MANGA if is_manga else GET_ANIME
    url = f'{ENDPOINT}/{param}/{item_id}'

    headers = {
        'Content-Type': 'application/json',
        'User-Agent': application_name
    }

    delay = random.uniform(0, 1)
    time.sleep(delay)

    try:
        result = requests.get(url, headers=headers).json()
    except Exception as e:
        print('Error', e, file=sys.stderr)
        return None

    return result


def download_many(item_ids: List[int], application_name: str, is_manga: bool = False):
    result = []

    for item_id in item_ids:
        item = download_single(item_id, application_name, is_manga)

        if item is not None:
            result.append(item)

    return result
