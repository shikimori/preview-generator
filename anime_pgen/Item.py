from datetime import datetime
from pathlib import Path

import requests

from anime_pgen.utils import eprint


class Item:
    type_dict = dict(
        tv='TV Сериал', movie='Фильм', ova='OVA', ona='ONA', special='Спешл', music='Клип',
        manga='Манга', light_novel='Ранобэ', novel='Новелла', one_shot='Ваншот', manhwa='Манхва', manhua='Маньхуа',
        doujin='Додзинси'
    )

    def __init__(self, item):
        en = False
        name_ru = item.get('russian', 'name')
        name_en = item.get('name')

        self.id = item.get('id', 0)
        self.en = en
        self.name_en = name_en

        self.population_date = datetime.now().isoformat()

        aired_on = item.get('aired_on', '')
        try:
            if aired_on:
                aired_on = datetime.fromisoformat(aired_on)
                self.year = aired_on.strftime('%Y')
                self.aired_on = True
            else:
                self.aired_on = None
        except Exception as e:
            print(e)
            self.aired_on = None

        self.kind = self.type_dict.get(item.get('kind'), None)
        self.is_manga = item.get('kind') in ['light_novel', 'novel', 'one_shot', 'manhwa', 'manhua', 'doujin', 'manga']

        if en:
            self.name = name_en
            self.en = True
            if not name_en:
                raise Exception('There is no name')
        else:
            if not name_en:
                raise Exception('There is no name')
            if name_ru == name_en:
                self.en = True
                self.name = name_ru
            if name_ru == '':
                self.name = name_en
                self.en = True
            else:
                self.name = name_ru

        self.image = item.get('image', {}).get('original')
        self.result_path = f'{self.id}.jpg'
        self.small_result_path = f's{self.id}.jpg'
        self.populated = True

        japanese = item.get('japanese')
        if japanese is not None and isinstance(japanese, list) and len(japanese) > 0:
            self.japanese = japanese[0]
        else:
            self.japanese = None

        if self.japanese == self.name_en:
            self.japanese = None

        self.score_text = item.get('score', '')
        self.score = float(item.get('score', '0.0'))

        description = item.get('description', '')

        if description is not None and description != '':
            self.description = item.get('description', '')
            self.description = ''.join(filter(lambda character: ord(character) < 0x3000, self.description))
            self.description = self.description.replace('[]', '')
            self.description = self.description.replace('[ ]', '')
        else:
            self.description = None

    def download(self, tmp_dir: Path, application_name: str):
        result = requests.get(
            url=f'https://shikimori.one{self.image}',
            headers={'User-Agent': application_name}
        )

        if result.status_code < 200 or result.status_code >= 300:
            eprint(result.content)
            return False

        filename = tmp_dir / f'{self.id}'

        with open(filename, 'wb') as f:
            f.write(result.content)

        self.image = str(filename)

        return True
