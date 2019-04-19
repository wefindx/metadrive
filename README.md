[![pypi](https://badge.fury.io/py/metadrive.svg)](https://badge.fury.io/py/metadrive)

# Metadrive
![alt txt](https://wiki.mindey.com/shared/screens/drivers.jpg)

Metadrive helps users gather the information from different Internet resources (e.g. [Linkedin](https://linkedin.com), [HTH Worldwide](https://hthworldwide.com), etc). It provides one API to rule them all. To gather the information from this or that resource there must be so called driver written especially for the resource. There are drivers which already exist. For example,
* Halfbakery: [halfbakery_driver](https://github.com/drivernet/halfbakery_driver)
* HTH Worldwide: [hthworld_driver](https://github.com/drivernet/hthworld_driver)
* Kompass: [kompass_driver](https://github.com/drivernet/kompass_driver)
* Linkedin: [linkedin_driver](https://github.com/drivernet/linkedin_driver)
* Metaculus: [metaculus_driver](https://github.com/drivernet/metaculus_driver)
* ResearchGate: [researchgate_driver](https://github.com/drivernet/researchgate_driver)
* Versli Lietuva: [verslilietuva_driver](https://github.com/drivernet/verslilietuva_driver)

Some of the drivers are awaiting to be implemented. Studying the Metadrive API will help developers to write the drivers for those resources which are needed them right now. A unified API is the killer feature of Metadrive and allows writing drivers to have a unified UI to the whole world.

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

### Installing drivers

After finishing the Metadrive installation you may check the drivers available right now.

```
$ curl http://127.0.0.1:7000/drivers
[]
```

So, there are no drivers and it's ok since they have to be installed separately.

Choose one of the above-mentioned drivers. Let's say it's `linkedin_driver`. Execute the following command to install it

```
pip install linkedin_driver
```

and run the second-to-last command one more time

```
$ curl http://127.0.0.1:7000/drivers
[{"id":"http://0.0.0.0:7000/driver/linkedin-driver","site":"https://www.linkedin.com","package":"linkedin-driver==0.1.8"}]
```

Here's the driver which has just been installed.

## Driver package structure:
```
.
├── driver_name
│   ├── __init__.py   # _login(), and an items generator function _harvest()
│   └── api.py        # classes, that define methods _get() and _filter() generators.
├── README.md
└── setup.py
```

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
