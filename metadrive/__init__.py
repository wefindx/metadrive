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


from typology.utils import get_schema


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
