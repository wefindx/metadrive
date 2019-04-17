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

## Installation

The guide provides for the instructions on how to install Metadrive to a virtual environment, so create and activate it first, running the following commands:

```
virtualenv -p python3.7 metadrive-env
. ./metadrive-env/bin/activate
```

Then, install Metadrive from its source code

```
git clone https://github.com/wefindx/metadrive.git
cd metadrive
pip install -e .
```

or from its package

```
pip install metadrive
```

Finally, run Metadrive, executing

```
provide
```

The command above will ask you to type your GitHub username. When you are done, the `.metadrive/config` will be created in your home directory and the server will start. The example of how `.metadrive/config` may look like:

```
[GITHUB]
username = mindey

[API]
host = 0.0.0.0
port = 7000

[CONSOLE]
host = 0.0.0.0
port = 7000

[DRIVER_BACKENDS]
chrome = /usr/bin/chromedriver
```

However, `provide` does not auto-reload and requires re-running, so if you want to run Metadrive for the development purposes, interrupt the `provide` process and execute the following command

```
uvicorn metadrive.api:app --debug
```

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
