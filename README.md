[![pypi](https://badge.fury.io/py/metadrive.svg)](https://badge.fury.io/py/metadrive)

# Metadrive
![alt txt](https://wiki.mindey.com/shared/screens/drivers.jpg)

Metadrive introduces simple generic interfaces to the objects within web APIs, allowing for generation (searching), and management of items on the web systems.

The drivers listed in [drivers.py](https://github.com/wefindx/metadrive/blob/master/metadrive/drivers.py) shall define controllers services and machines, to serialize data in [MFT-1](https://book.mindey.com/metaformat/0002-data-object-format/0002-data-object-format.html), making them convenient to automatically operate with [metaform](https://pypi.org/project/metaform/)). This list of drivers is to be provided in a distributed fashion, i.e., with GunDB.

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

## Prepare machine
```
sudo apt install virtualenv python3.7 python3.7-dev build-essential chromium-browser chromium-chromedriver
```

## Develop
```
git clone git@github.com:wefindx/metadrive.git && cd metadrive
git submodule update --init --recursive
virtualenv -ppython3.7 .env && . .env/bin/activate
pip install -e .
```
### First run
```
$ provide
```

```
uvicorn metadrive.api:app --debug
```
### To incorporate the latest data-browser
```
git update-index --cacheinfo 160000,<commit hash of data browser repo>,metadrive/_ui_scripts
```

### Default ~/.metadrive/.config example:
`docker run -d -p 4444:4444 selenium/standalone-chrome`

```
[GITHUB]
username = mindey

[API]
host = 0.0.0.0
port = 7000

[CONSOLE]
host = 0.0.0.0
port = 7001

[DRIVER_BACKENDS]
chrome = http://0.0.0.0:4444/wd/hub

[GPG]
key = 5AFDB16B89805133F450688BDA580D1D5F5CC7AD

[PROXIES]
http =
https =
```


## Usage

Basic Installation:
```
pip install metadrive
```

(check installation requirements for specific systems at the bottom)

## Driver package structure:
```
.
├── driver_name
│   ├── __init__.py   # _login(), and an items generator function _harvest()
│   └── api.py        # classes, that define methods _get() and _filter() generators.
├── README.md
└── setup.py
```

### Defualt files structure

```
__init__.py file:
=====================
 _login(): authentication function

 _harvest(): default downloading function

api.py file:
============
 Classes represent data types available in data source of driver package.
 Methods represent way to query for objects in the data source.

 @classmethod
 _filter(): Returns a generator of the objects of the class.

 @classmethod
 _get(): Returns a method to retrieve a single object.

 @classmethod
 _update(): A method to update or delete the object in source by ID.
```

1. Publish drivers on `PyPI`.

2. Reference them on `-` wikis on GitHub (example: [https://github.com/mindey/-/wiki/topic#halfbakery](https://github.com/mindey/-/wiki/topic#halfbakery).

3. Use, like `harvest https://github.com/mindey/-/wiki/topic#halfbakery -o my_data`.

Alternatively, to database:
`harvest https://github.com/user/-/wiki/concept\#source --db mongodb://username:password@hostname:27017/db_name/collection`

More advanced usage will be covered in the future.

## Android

If installed on Termux (Android), needs:
```
pkg i clang
pkg i make
pkg i python-dev
pkg i libcrypt-dev
pkg i libffi-dev
pkg i openssl
pkg i openssl-dev
pkg i openssl-tool
pkg i libjpeg-turbo-dev
LDFLAGS="-L/system/lib/" CFLAGS="-I/data/data/com.termux/files/usr/include/" pip install Pillow
OR LIBRARY_PATH="/system/lib" CPATH="$PREFIX/include" pip install pillow
```
## Extras

As a plugin, data normalization package is available, to use it, install:
```
pip install -U --extra-index-url https://pypi.wefindx.io/ metaform --no-cache
```

then, pass `?normalize=true` as URL parameter as part of `POST` requests. The data `results` key will be normalized.

## Authors

See [AUTHORS](AUTHORS.md).

## Licensing

metadrive is available under the [Apache License, Version 2.0](LICENSE).
