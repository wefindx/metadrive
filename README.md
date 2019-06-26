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
  * [Installing drivers](#installing-drivers)
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
virtualenv -p python3 metadrive-env
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
connect <resource>
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

### Installing drivers

Drivers are automatically installed, when a drive is requested and a driver exists.

```
import metadrive
drive = metadrive.drives.get('halfbakery-driver:Mindey')

## Documentation

The documentation for Metadrive can be found at [https://metadrive.readthedocs.io](https://metadrive.readthedocs.io/en/latest/).

## Authors

See [AUTHORS](AUTHORS.md).

## Licensing

metadrive is available under the [Apache License, Version 2.0](LICENSE).
