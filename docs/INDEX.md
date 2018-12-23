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

Use `pip install --editable .` to preview changes to the commands.

# Structure

Metadrive structure is intended to be self-explanator. That said, to operate on every specific machine or site, we use specific repositories, that depend on `metadrive`, and each of them has to have the following structure:

```
driver
    __init__.py
    api.py
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
class ThingA:
    namespace = '::someone/thing#1'
    def method1():
       ...
    def method2():
       ...

class ThingB:
    namespace = 'https://github.com/someone/-/wiki/thing#N'
    def method1():
       ...
    def method2():
       ...
```

For example, if Mindey decided to crawl Wikipedia topics in his own way, it may be something like:

```
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

