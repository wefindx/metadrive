[![build](https://travis-ci.org/wefindx/metadrive.svg?branch=master)](https://travis-ci.org/wefindx/metadrive)
[![pypi](https://badge.fury.io/py/metadrive.svg)](https://badge.fury.io/py/metadrive)

# Metadrive
![alt txt](https://wiki.mindey.com/shared/screens/drivers.jpg)

Metadrive helps control information from different Internet resources (e.g. [Linkedin](https://linkedin.com), [Halfbakery](https://www.halfbakery.com), etc). It provides one API to rule them all at the operating system filesystem level, via allowing to mount and syncing web resources, as if they are disks (mounted filesystems) on your operating system. To gather the information from a specific resource, there must be so called driver written specifically for the resource. There are drivers which already exist. For example,
* Halfbakery: [halfbakery_driver](https://github.com/drivernet/halfbakery_driver)
* Linkedin: [linkedin_driver](https://github.com/drivernet/linkedin_driver)
* Metaculus: [metaculus_driver](https://github.com/drivernet/metaculus_driver)
* HTH Worldwide: [hthworld_driver](https://github.com/drivernet/hthworld_driver)
* Kompass: [kompass_driver](https://github.com/drivernet/kompass_driver)
* ResearchGate: [researchgate_driver](https://github.com/drivernet/researchgate_driver)
* Versli Lietuva: [verslilietuva_driver](https://github.com/drivernet/verslilietuva_driver)

Many drivers are awaiting to be implemented at [drivernet][https://github.com/drivernet]. Studying the Metadrive will help developers to write the drivers for those resources which are needed them right now. A unified API is the killer feature of Metadrive and allows writing drivers to have a unified UI to the whole world.

## Table of Contents

- [Prepare machine](#prepare-machine)
- [Installation](#installation)
- [Documentation](#documentation)
- [Authors](#authors)
- [Licensing](#licensing)

## Prepare machine
```
sudo apt install virtualenv python3 python3-dev build-essential chromium-browser chromium-chromedriver pandoc
```

## Installation

The guide provides for the instructions on how to install Metadrive to a virtual environment, so create and activate it first, running the following commands:

```
pip install metadrive
```

Note: by default, all sessions are stored at `~/.metadrive/sessions/`, under the subfolder of underscored "metadrive", e.g., `_selenium` default session is at `~/.metadrive/sessions/_selenium/default`, or `_requests` default session data is at `~/.metadrive/sessions/_requests/default`

## Usage

### If you want to mount resources
Mounting site to `~/Sites` or to custom location:
```
drive halfbakery.com # defaults to /home/<user>/Sites
drive halfbakery.com /my/custom/location
```


The command above will ask you to type your GitHub username. When you are done, the `.metadrive/config` will be created in your home directory and the server will start. The example of how `.metadrive/config` may look like:

```
[GITHUB]
username = mindey

[DRIVER_BACKENDS]
chrome = /usr/bin/chromedriver

[PROXIES]
http =
https =

[GPG]
key = 5AFDB16B89805133F450688BDA580D1D5F5CC7AD
```

### If you want to use resources in code

```
import metadrive
```

#### Minimal, with 'default' session in `~/.metadrive/session/<metadrive>/default`:

```
# Examples:

drive = metadrive._requests.get_drive()                # metadrive: 'requests', driver: None, profile: 'default'
drive = metadrive._requests.get_drive(profile='novel') # metadrive: 'requests', driver: None, profile: 'novel'
drive = metadrive._selenium.get_drive(headless=False)  # metadrive: 'selenium', driver: None, profile: 'default'
```

#### If you want to use a custom driver interface with default session, e.g.:

```
# Examples:
drive = metadrive.drives.get('halfbakery-driver')          # metadrive: implied, driver: halfbakery-driver, profile: 'default'
drive = metadrive.drives.get('halfbakery-driver:SomeName') # metadrive: implied, driver: halfbakery-driver, profile: 'SomeName'
```

This installs the `pip install halfbakery-driver`, and uses it. Each driver has to have `.__site_url__` attribute, and this way, metadrive determines which resource requires which driver to read.


The documentation for Metadrive can be found at [https://metadrive.readthedocs.io](https://metadrive.readthedocs.io/en/latest/).

## Authors

See [AUTHORS](AUTHORS.md).

## Licensing

metadrive is available under the [Apache License, Version 2.0](LICENSE).
