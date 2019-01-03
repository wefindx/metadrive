# Metadrive

## Usage

Basic Installation:
```
pip install -U -i https://metaformat:internationalcooperationhappens@pypi.wefindx.io metadrive
```

Driver structure:
```
.
├── driver_name
│   ├── __init__.py   # login(), and an items generator function with optional name.
│   └── api.py        # classes, that define methods available to crawled items.
├── README.md
└── setup.py
```

1. Publish drivers on `PyPI`.

2. Reference them on `-` wikis on GitHub (example: [https://github.com/mindey/-/wiki/topic#halfbakery](https://github.com/mindey/-/wiki/topic#halfbakery).

3. Use, like `harvest https://github.com/mindey/-/wiki/topic#halfbakery`.

More advanced usage will be covered in the future.

## About

The package that introduces simple generic interfaces to the objects within web APIs, allowing for generation (searching), and management of items on the web systems.

The drivers listed in `drivers.py` shall define controllers services and machines, to serialize data in [MFT-1](https://book.mindey.com/metaformat/0002-data-object-format/0002-data-object-format.html), making them convenient to automatically operate with [metaform](https://pypi.org/project/metaform/)). This list of drivers is to be provided in a distributed fashion, i.e., with GunDB.

When writing drivers, optionally define `login()` function, and some generator function `harvest(limit=limit)` function in `__init__.py`. The generator function needs to return elements, where `-` key is the URL of the items.

Installation may require `ncurses`.

`$ harvest <resource>`
The first command allows to crawl custom source.

`$ provide`
The second command serves the API to the APIs and data.

`$ console`
Starts console application with `get(), list(), update()` methods to manage index of all available controllers ( drivers ), and get data.

`$ consume`
Starts a GUI-based application to manage index of all available controllers ( drivers ), and interact with data objects visually.


# TODO

## Web information services

**Industrial and Medical Equipment**
**Metal printers** ([https://www.aniwaa.com/best-of/3d-printers/best-metal-3d-printer/#The_best_metal_3D_printers_in_2018](https://www.aniwaa.com/best-of/3d-printers/best-metal-3d-printer/#The_best_metal_3D_printers_in_2018)), **CNC Machines** ( [https://github.com/Nikolay-Kha/PyCNC#readme](https://github.com/Nikolay-Kha/PyCNC#readme), [https://mmi-direct.com/machines/search/?make_id=&page=brand](https://mmi-direct.com/machines/search/?make_id=&page=brand)).

**Products**
Taobao, 天猫, Alibaba, Amazon, EBay,...

**Business data**
￼
Flights ( flightradar24.com ), Skyscanner ( skyscanner.com ), Weather ( windy.com ), Human ( biodigital.com ), Ships ( marinetraffic.com ), Deaths ( https://www.cdc.gov/nchs/data_access/vitalstatsonline.htm ), Companies ( opencorporates.com, etc.), Oil Miners ( http://aleph.openoil.net/ ),...

**Common services**
Gmail API ( get all your mails ), LinkedIn, Google Plus, Twitter, Weibo, Telegram, WeChat, Kik, KakoTalk, Line, WhatsApp, Quora, Kr36, MeetUp, 知乎, Huodongxing, YouTube, YouKu, Vimeo,...

## Private PyPI repository of drivers
## Private organization '-' repository
