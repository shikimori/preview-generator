# Генератор превью для Shikimori
![Демо](https://github.com/shikimori/preview-generator/raw/master/demo.gif)

<p align="center"><i>Демо</i></p>

[![pypi](https://img.shields.io/pypi/v/anime-pgen?color=%2334D058&label=pypi%20package)](https://pypi.org/project/anime-pgen)


## Описание
`anime-pgen` представляет собой `cli`-утилиту для генерации превью-изображений по данным Шикимори (_скачивание данных включено в функциональность_). В качестве фреймворка для организации `cli` интерфейса используется [Typer](https://typer.tiangolo.com)

### Требования и установка

- Python `^3.9`
- `pip`, или, `poetry` или любой другой пакетный менеджер для Python
- Приложение на [Shikimori](https://shikimori.one/oauth/applications) (_для работы необходимо иметь_ `APPLICATION_NAME`)

Установка:
```bash
$> pip install anime-pgen
```

[Опционально] Подсказки для терминала:
```bash
$> pgen --install-completion
```


## Использование

1. Понадобится создать папку для конфигов и контента
```bash
$> mkdir previews && cd previews
```

2. Далее нужно добавить конфиг-файл. Его можно взять [в репозитории](https://github.com/shikimori/preview-generator/blob/master/config.example.yaml). Имя файла: `config.yaml`
```bash
$> cp config.example.yaml config.yaml
$> l
total 16
drwxr-xr-x   4 user  staff   128B Jun 28 19:48 .
drwxr-xr-x  23 user  staff   736B Jun 28 19:43 ..
-rw-r--r--   1 user  staff   1.1K Jun 28 19:48 config.yaml
```

3. Для удобства создадим папку `content` - в ней разместим шрифты и иконки
```bash
$> mkdir content
$> l
total 16
drwxr-xr-x   5 user  staff   160B Jun 28 19:52 .
drwxr-xr-x  23 user  staff   736B Jun 28 19:49 ..
-rw-r--r--   1 user  staff   1.1K Jun 28 19:48 config.yaml
drwxr-xr-x   2 user  staff    64B Jun 28 19:52 content
```

4. В новосозданную папку `content` можно сразу [перенести из репозитория](https://github.com/shikimori/preview-generator/tree/master/content) двусоставное лого Шикимори, иконку рейтинга и заполнение заднего фона (или можно использовать свои)
```bash
$> cp shikimori-glyph.png content/shikimori-glyph.png
$> cp shikimori-logo.png content/shikimori-logo.png
$> cp star.png content/star.png
$> cp tile.png content/tile.png
$> tree -a
.
└── previews
    ├── config.yaml
    └── content
        ├── shikimori-glyph.png
        ├── shikimori-logo.png
        ├── star.png
        └── tile.png
```

5. В `content` так же нужно положить шрифты. Для Шикимори используются:
	- [🔗](https://fonts.google.com/specimen/Open+Sans) `OpenSans` для заголовка и описания
	- [🔗](https://docs.microsoft.com/ru-ru/typography/font-list/tahoma) `Tahoma` для рейтинга
	- [🔗](https://fonts.google.com/noto/specimen/Noto+Serif+JP) `NotoSerif_JP` для Японских иероглифов

Финально папка `previews` выглядит примерно так:
```bash
$> tree -a -L 4
.
└── previews
    ├── config.yaml
    └── content
        ├── Noto_Serif_JP
        │   ├── NotoSerifJP-Black.otf
        │   ├── NotoSerifJP-Bold.otf
        │   ├── NotoSerifJP-ExtraLight.otf
        │   ├── NotoSerifJP-Light.otf
        │   ├── NotoSerifJP-Medium.otf
        │   ├── NotoSerifJP-Regular.otf
        │   ├── NotoSerifJP-SemiBold.otf
        │   └── OFL.txt
        ├── Open_Sans
        │   ├── LICENSE.txt
        │   ├── OpenSans-Italic-VariableFont_wdth,wght.ttf
        │   ├── OpenSans-VariableFont_wdth,wght.ttf
        │   ├── README.txt
        │   └── static
        ├── Tahoma
        │   ├── COPYRIGHT.txt
        │   └── tahoma.ttf
        ├── shikimori-glyph.png
        ├── shikimori-logo.png
        ├── star.png
        └── tile.png

```

### `config.yaml`

Рассмотрим конфигурационный файл. По дефолту он выглядит так:
```yml
size: 'big'

colors:
  background: '#ffffff'
  text: '#343434'
  year: '#555555' 

  rating:
    active: '#4c86c8'
    regular: '#cccccc'

content:
  images: 
    background_tile: content/tile.png 
    star: content/star.png 
    logo: 
      glyph: content/shikimori-glyph.png
      text: content/shikimori-logo.png
  fonts: 
    text: content/Open_Sans/OpenSans-VariableFont_wdth,wght.ttf
    bold_text: content/Open_Sans/static/OpenSans/OpenSans-Bold.ttf
    numbers: content/Tahoma/tahoma.ttf
    japanese: content/Noto_Serif_JP/NotoSerifJP-Bold.otf 
```
---
```yml
size: 'big'
```

Возможные значения:
  - `big`   = 1200 x 630 _(значение по умолчанию)_
  - `small` = 600 x 315

Это размер финального изображения. Цифры являются рекоммендацией к формату превью от Facebook/Twitter/Вконтакте.

----

```yml
rating:
    active: '#4c86c8'
    regular: '#cccccc'
```
Цвета звёздочек рейтинга - активных и плейсхолдеров.
В конфиге представлены их дефолтные значения.

----

```yml
colors:
  background: '#ffffff'
  text: '#343434'
  year: '#555555' 
```

Цвета:
- Подложки (`background`)
- Всего текса (`text`)
- Года выпуска (`year`)

В конфиге представлены их дефолтные значения.

----

**Важно!**

`colors` и `size` - опциональны. 
В случае, если они не указаны в файле - будут использовать дефолтные значения (которые совпадают с дефолтным конфигом)

`content` - обязательные поля

**Важно2!**
Для картинок нельзя использовать `.svg`, только `.jpeg|.jpg|.png` (ограничение библиотеки)

----

```yml
content:
  images: 
    background_tile: content/tile.png 
```

Путь до файла с тайлом для заднего фона. Например, дефолтный для Шикимори:

![Tile](https://shikimori.one/assets/background/square_bg.png)

Рекоммендации:
- Квадратный (иначе сплющится)
- Бесшовный
- `.png` с альфа-каналом, если хочется красивого наложения на белый фон

----

```yml
content:
  images: 
    star: content/star.png 
```
Путь до файла со звездой рейтинга.

Требования:
- Прозрачный фон
- Фигура чёрного цвета
- Квадрат

При накладывании на превью чёрный цвет перекрашивается в `rating.active` или `rating.regular`

----

```yml
logo: 
      glyph: content/shikimori-glyph.png
      text: content/shikimori-logo.png
```

Двусоставное лого Шикимори - Иероглиф + "SHIKIMORI"

Требования:
- Одинаковая высота
- `.png` с альфа-каналом

----

```yml
fonts: 
    text: content/Open_Sans/OpenSans-VariableFont_wdth,wght.ttf
    bold_text: content/Open_Sans/static/OpenSans/OpenSans-Bold.ttf
    numbers: content/Tahoma/tahoma.ttf
    japanese: content/Noto_Serif_JP/NotoSerifJP-Bold.otf 
```

Путь до шрифтов:
- `text` - описание и подписи
- `bold_text` - название
- `number` - рейтинг и год
- `japanese` - для Иероглифов, Хираганы и Катаканы

Требования:
- `TrueType` шрифты

### Использование

- Подробная документация по `cli`-интерфейсу: [DOCS.md](https://github.com/shikimori/preview-generator/blob/master/DOCS.md)
- Пример использования: [Makefile](https://github.com/shikimori/preview-generator/blob/master/Makefile)

Использование состоит из двух частей:
1. Скачиваем данные из API-Шикимори по `id` аниме или манги
2. Генерируем превью по данным

Скачаем информацию об аниме "Ковбой Бибоп":
```bash
$> pgen fetch 1 --app-name <APPLICATION_NAME_из_Шикимори>
Successfully saved to .pgen.json

$> l
total 40
drwxr-xr-x  6 vladimirlevin  staff   192B Jun 28 20:36 .
drwxr-xr-x  3 vladimirlevin  staff    96B Jun 28 19:56 ..
-rw-r--r--  1 vladimirlevin  staff   9.2K Jun 28 20:36 .pgen.json
-rw-r--r--  1 vladimirlevin  staff   1.1K Jun 28 19:48 config.yaml
drwxr-xr-x  9 vladimirlevin  staff   288B Jun 28 20:03 content
```

По умолчанию данные сохраняются в `.pgen.json`, путь можно изменить, передав флаг `--save-path 'my_file.json'`
```bash
$> pgen fetch 1 --app-name <APPLICATION_NAME_из_Шикимори> --save-path "my_file.json"
Successfully saved to my_file.json
```

Переходим к генерации:
```bash
$>pgen make-preview .pgen.json \
	--output-folder "." \
    --config "config.yaml" \
    --app-name <APPLICATION_NAME_из_Шикимори>

Successfully create previews:
         - 1.jpg
```

**Готово!** 🥳

### FAQ

**Q**: Как разметить много за раз? <br>
**A**: С флагом `-M` можно за раз скачать и разметить много Аниме/Манги:
```bash
$> pgen fetch -M "1,5,8" --app-name <APPLICATION_NAME_из_Шикимори>
Successfully saved to .pgen.json

$> pgen make-preview .pgen.json --output-folder "." --config "config.yaml" --app-name <APPLICATION_NAME_из_Шикимори>
Successfully create previews:
         - 1.jpg
         - 5.jpg
         - 8.jpg
```

**Q**: Как разметить мангу?<br>
**A**: С помощью флага `-m` можно скачать Мангу. Создание превью опирается на данные, поэтому во второй команде ничего не потребуется менять
```bash
$> pgen fetch -mM "1,8" --app-name <APPLICATION_NAME_из_Шикимори>
Successfully saved to .pgen.json

$> pgen make-preview .pgen.json --output-folder "." --config "config.yaml" --app-name <APPLICATION_NAME_из_Шикимори>
Successfully create previews:
         - 1.jpg
         - 8.jpg
```
