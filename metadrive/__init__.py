import pkgutil
import importlib

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


    SUPPORTED_PACKAGE_MANAGERS = ['pypi']

    if reader.lower().split(':',1)[0] not in SUPPORTED_PACKAGE_MANAGERS:
        raise Exception(
            "Unknown package manager. " +
            "Make sure the reader you chose starts with one of these: " +
            "{}. Your chosen reader is: {}".format(
                ', '.join(SUPPORTED_PACKAGE_MANAGERS),
                reader
            )
        )

    SUPPORTED_PACKAGES = [
        'pypi:metadrive',
        'pypi:drivers',
        'pypi:subtools'
    ]

    package_name = reader.split('.', 1)[0].lower()

    if package_name not in SUPPORTED_PACKAGES:
        raise Exception(
            "Unsupported reader package. " +
            "Make sure the reader package is one of these: " +
            "{}. Your chosen reader is: {}".format(
                ', '.join(SUPPORTED_PACKAGES),
                package_name
            )

        )

    packman, package = package_name.split(':')

    # Make sure we have that package installed.
    spec = importlib.util.find_spec(package)
    if spec is None:
        answer = input(package +" is not installed. Install it? [y/N] ")
        if answer in ['y', 'Y']:
            try:
                #easy_install.main( ["-U", package_name] )
                os.system('pip install --no-input -U {} --no-cache'.format(package))
            except SystemExit as e:
                pass
        else:
            raise Exception(package_name +" is required. Install it and run again.")
    else:
        # Check the version installed.
        import pkg_resources
        importlib.reload(pkg_resources)
        installed_version = pkg_resources.get_distribution(package).version

        # Check the latest version in PyPI
        from yolk.pypi import CheeseShop

        def get_lastest_version_number(package_name):
            pkg, all_versions = CheeseShop().query_versions_pypi(package_name)
            if len(all_versions):
                return all_versions[0]
            return None

        latest_version = get_lastest_version_number(package)


        def cmp_version(version1, version2):
            def norm(v):
                return [int(x) for x in re.sub(r'(\.0+)*$','', v).split(".")]
            return cmp(norm(version1), norm(version2))

        if latest_version is not None:
            if cmp_version(installed_version, latest_version) < 0:
                print(latest_version, type(latest_version))
                answer = input('You are running {}=={}'.format(package,installed_version)+", but there is newer ({}) version. Upgrade it? [y/N] ".format(latest_version))
                if answer in ['y', 'Y']:
                    try:
                        os.system('pip install --no-input -U {} --no-cache'.format(package))
                    except SystemExit as e:
                        pass




    module = __import__(package)

    # Get method and package:
    namespace = reader.split('.', 1)[-1]

    method = module
    for name in namespace.split('.'):
        method = getattr(method, name)

    return method(limit=limit)
