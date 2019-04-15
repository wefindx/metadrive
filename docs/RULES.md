# RULES 0.1

## Terminology

- `resource`: any addressable system with I/O capabilities.
- `driver`: a package, that implements the below `Package Rules`.
- `drive`: a pair of driver package name and session data, encoded and stored as an encapsuled unit in isolated location
- `subtool`: an property of metadrive, that implements a middleware and extension of a generic package, like selenium, ansible, etc., by providing (MUST) `get_drive` method, that returns a `drive` ([example](https://github.com/wefindx/metadrive/blob/master/metadrive/_requests.py#L12)), that binds session data with driver.
- `types`: term describing groups of classes of things, that can have instances. (For example, term: user, class: AirBnbUser, instance: Joe) 

## Package Rules

In order to make your software package available as a metadrive API module, the package MUST be a driver dedicated for interacting with an addressable web `resource`, that is:

1. It MUST have `__site_url__` property as the property of imported package name. Additionally:
2. It MUST have `_login` function as property of imported package, that returns an instance of `drive` defined in the driver package that uses generic `get_drive` function from a `subtool` of metadrive.
3. It MUST have `api` attribute as property of imported package, that has at least one `class` corresponding with to a `type` of objects available in the `resource`, such that:
  - Each `class` MUST inherit from a `dict` subtype defined in [metatype](https://github.com/wefindx/metatype/) package,
     - and MUST have `-` or `url` key specifying their *data item origin location*, as per [MFT-1](https://book.mindey.com/metaformat/0002-data-object-format/0002-data-object-format.html) specification.
     - and MAY have `*`, `+`, `^` keys specifying their *schema*, *keys and permissions*, and *itention* respectively as per [MFT-1](https://book.mindey.com/metaformat/0002-data-object-format/0002-data-object-format.html) specification.
  - Each `class` MUST have `@classmethod` method named `_filter`, that returns a generator for class instances.
  - Each `class` MAY have `@classmethod` method named `_get`, that returns an instance of class.
  - Each `class` MAY have `@classmethod` method named `_update`, that allows creating/modifying/deleting of class instances in `resource`.
4. It MAY have `_harvest` function as the property of imported package, that returns a generator, made for dumping all data (full crawl) from resource.
