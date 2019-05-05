import yaml
import pkgutil
import inspect
import re

from metadrive import utils

__all__ = []
for loader, module_name, is_pkg in  pkgutil.walk_packages(__path__):
    __all__.append(module_name)
    _module = loader.find_module(module_name).load_module(module_name)
    globals()[module_name] = _module

import os, config

if not os.path.exists(config.DEFAULT_LOCATION):
    os.makedirs(config.DEFAULT_LOCATION)


from metaform import get_schema
from metadrive import drives

def search(source, features: dict):
    '''
    Object discovery by features in source.

    Accepts:
        source: drive and class, e.g. linkedin-driver:default.api.Post
        features: object dictionary of serialized object

    Returns:
        generator of objects.

    Note: url itself is a feature, too.
    '''
    raise NotImplemented

def create(source, features: dict):
    '''
    Object creation by features in source.

    Accepts:
        source: drive and class, e.g. linkedin-driver:default.api.Post
        features: dictionary of serialized object.

    Returns:
        object's address, and success status and/or errors.
    '''
    raise NotImplemented

def load(data):
    '''
    takes: saved data item
    returns: item instnace of the class from driver
    '''
    if isinstance(data, str):
        data = yaml.load(open(data, 'r'))

    _id = data.get('-')
    _drive = data.get('@')

    if _id is not None and _drive is not None:

        # parsing '@' field:                                    #sample: PyPI::halfbakery_driver==0.0.1:default.api.Topic

        # TBD: refactor by importing from metatype
        packman = _drive.split('::', 1)[0]                 #sample: PyPI  (Conan, NPM, Paket, etc.)
        drivespec = _drive.split('::', 1)[-1]              #sample: halfbakery_driver==0.0.1:default.api.Topic
        driver_name_version = drivespec.split(':',1)[0]         #sample: halfbakery_driver==0.0.1
        driver_name = driver_name_version.split('==',1)[0]      #sample: halfbakery_driver
        driver_version = driver_name_version.rsplit('==',1)[-1] #sample: 0.0.1
        profile_name_pkg_path = drivespec.rsplit(':',1)[-1]     #sample: default.api.Topic
        profile_name = profile_name_pkg_path.split('.',1)[0]    #sample: default
        pkg_path = profile_name_pkg_path.split('.',1)[-1]       #sample: api.Topic

        # TBD: refactor by reusing metadrive/api.py# around 90 line
        ndriver = driver_name.replace('-', '_')
        module = __import__(ndriver)
        api = __import__('{}.api'.format(ndriver), fromlist=[ndriver])
        classname = _drive.rsplit('.',1)[-1]
        Klass = getattr(api, classname)

        item = Klass(data)
        item.drive = drives.get('{}:{}'.format(driver_name, profile_name))
        return item


def read(term, limit=None):
    '''
    calls '_:emitter'

    Reads term as source, where there is '_:emitter' attribute.

    The attribute has to specify one or more functions, that are generators of Dict objects.

    Examples:
    >>> read('::mindey/topic#halfbakery')
    >>> read('https://github.com/mindey/-/wiki/topic#halfbakery')
    '''
    template = get_schema(term)

    readers = template.get('_:emitter')

    if not readers:
        raise Exception('Readers not found in template.')

    if isinstance(readers, list):

        for i, reader in enumerate(readers):
            print(i+1, reader)

        reader_id = input("Choose reader [1] ")

        if not reader_id:
            reader_id = 1
        else:
            reader_id = int(reader_id)

        if reader_id not in range(1, len(readers)+1):
            raise Exception("The choice does not exist.")

        reader_id -= 1
        reader = readers[reader_id]

    elif isinstance(readers, str):
        reader = readers
    else:
        raise Exception("Reader defined as anything other than string or list is not supported.")


    package = utils.ensure_driver_installed(reader)


    module = __import__(package)

    # Get method and package:
    namespace = reader.split('.', 1)[-1]

    method = module
    for name in namespace.split('.'):
        method = getattr(method, name)

    method_args = inspect.getfullargspec(method).args

    if 'limit' in method_args:
        return method(limit=limit)
    else:
        return method()
