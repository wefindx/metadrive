# Metadrive

The package that introduces simple generic interfaces to the objects within web APIs, allowing for generation (searching), and management of items on the web systems.

The drivers shall define clients for [metaform](https://pypi.org/project/metaform/).

`$ harvest <resource>`
The first command allows to crawl custom source.

`$ provide`
The second command serves the API to the APIs and data.

Use `pip install --editable .` to preview changes to the commands.

# Structure

Metadrive contains:

```
metadrive/
    service1
        __init__.py
        api.py
    service2
        __init__.py
        api.py
    ...
    serviceN
        __init__.py
        api.py
    _tool1.py
    _tool2.py
    ...
    _toolN.py - pre-configured drivers for metatools (protocol-level interfaces to tools)
```

## The `__init__` files provide:

Variables
`__site_url__` - a variable that specifies the site url, that provides site's UI (user interface).  The reason why we need it, is because, e.g., if we open a site via `"data browser"` relying metadrive, we can just enter the familiar url of the service.
`__base_url__`, - a variable that specifies the site's API (application programming interface), if available.

Functions
`login()` - a function that provides a way to sign-in to resource.
`search()` - a function that provides doing arbitrary queries to retrieve limited sections of data.
`generate()` - a function that implements one-off non-stop continual crawling of the whole resource.

## The `api.py` files provides:

The internal structure of the objects within the service. For example:

```
class Thing1:
    namespace = '::someone/thing#1'
    def method1():
       ...
    def method2():
       ...

class ThingN:
    namespace = 'https://github.com/someone/-/wiki/thing#N'
    def method1():
       ...
    def method2():
       ...

For example, if Mindey decided to crawl Wikipedia topics in his own way, it may be something like:

class Topic:
    namespace = '::mindey/topic#wikipedia'
    def method1():
       ...
    def method2():
       ...
```

The `search()` and `generate()` are generators, that must produce data records that follow metaformat ([MFT-1](https://book.mindey.com/metaformat/0002-data-object-format/0002-data-object-format.html)) specifications, which means, records **must** have `*` field, that specifies the url of schema, and **may** have `-`, `+`, `^` fields, that specify location, authentication and permissions, and author intent urls.

To understand the links to `namespace` specified in the objects in the `api.py`, we have shorthands the metawiki (`pip install metawiki`) provides mapping [map.py](https://github.com/mindey/metawiki/blob/master/metawiki/map.py) for `namespaces` for MFT-1. Under metawiki namespaces, the `-:` provides links to folders, while `::` provides links to wiki of a GitHub repo. For example, if the GitHub username is `someone`, then `metawiki.name_to_url('::someone/transaction#service_name')` results in `https://github.com/someone/-/wiki/transaction#service_name'`. (Everyone can create concept definitions under `-` repo wiki of their Github user, or just provide namespace URL.)

This is useful for records, that also have authentication data url in `+` field, that makes it possible to call methods on data records, no matter where the data is. The authentication data is stored on-line, on `+` folder on `-` repository. For example, `https://github.com/mindey/-/tree/master/+` (or, for example `metawiki.name_to_url('-:mindey/+/test.md')`), encrypted with GPG (e.g., `pip install gpgrecord`, and `gpgrecord.encrypt_data({'key': 'value'}, ['fingerprint1', 'fingerprint2',...])`.)

The sessions are stored locally in `sessions` folder, under `~/.metadrive` dot-folder, where the repos `-` is checked out to the `~/.metadrive/-` of the user specified via automation in the `config.py`, that generates `~/.metadrive/config` file, that specifies the default `GITHUB` username, and `GPG` key of the local user.

The schema and authentication/permissions data could be stored anywhere by providing arbitrary URLs, where we store the data, but then, the automation here would have to reviewed a little.

# TODO

# Social information services

## Products
1. Taobao
2. 天猫
3. Alibaba
4. Amazon
5. EBay

## Business data
￼
1. Flights ( flightradar24.com )
2. Skyscanner ( skyscanner.com )
3. Weather ( windy.com )
4. Human ( biodigital.com )
5. Ships ( marinetraffic.com )
6. Deaths ( https://www.cdc.gov/nchs/data_access/vitalstatsonline.htm )
7. Companies ( opencorporates.com, etc.)
8. Oil Miners ( http://aleph.openoil.net/ )
￼
## Common services
1. Gmail API ( get all your mails )
2. LinkedIn
3. Google Plus
4. Twitter
5. Weibo
6. Telegram
7. WeChat
8. Kik
9. KakoTalk
10. Line
11. WhatsApp

## Common
1. Quora
2. Kr36
3. MeetUp
4. 知乎
5. Huodongxing

## Video
1. YouTube
2. YouKu
3. Vimeo

# Industrial and Medical Equipment

## Metal printers

- [https://www.aniwaa.com/best-of/3d-printers/best-metal-3d-printer/#The_best_metal_3D_printers_in_2018](https://www.aniwaa.com/best-of/3d-printers/best-metal-3d-printer/#The_best_metal_3D_printers_in_2018)

## CNC Machines

**Note:** [https://github.com/Nikolay-Kha/PyCNC#readme](https://github.com/Nikolay-Kha/PyCNC#readme)

- [https://mmi-direct.com/machines/search/?make_id=&page=brand](https://mmi-direct.com/machines/search/?make_id=&page=brand)

## Development
Add `~/.pypirc` file:

```
[distutils]
index-servers =
  pypi
  internal

[pypi]
username:<your_pypi_username>
password:<your_pypi_passwd>

[internal]
repository: https://pypi.wefindx.io
username: <wefindx_pypi_username>
password: <wefindx_pypi_passwd>
```

Then, use:
`python setup.py sdist upload -r internal`

Or also, use:
`pip install -i https://pypi.wefindx.io metadrive`


And then, `requirements.txt` may look like so:
`
metadir==0.0.1
--extra-index-url https://<wefindx_pypi_passwd>@ypi.wefindx.io/<wefindx_pypi_username>/
metadrive==0.4.0
`
