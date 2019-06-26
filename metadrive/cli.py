import click
import importlib
import json
import metadrive
from metadrive import utils
from typology.utils import slug
from metawiki import name_to_url
import os
from urllib.parse import urlparse
from metadrive.config import (
    ENSURE_SITES,
    SITES_DIR,
)
from metadrive.mnt import mount

# Cause ecryptfs supports max 143 chars.
FILENAME_LENGTH_LIMIT = 143


@click.command()
@click.argument('resource', required=True, metavar='<resource>')
@click.argument('mountpoint', required=False, metavar='<mountpoint>')
@click.option('-u', '--user', required=False, type=str, help='Reuse a drive by name.')
@click.option('-p', '--period', required=False, type=float, help='Period of resynchronization in number of seconds.')
def connect(resource, mountpoint=None, user=None, period=900):
    """
    Mounts interactive data from a resource as a filesystem to OS.
    $ connnect <resource> [location]
    """
    if period is None:
        period = 900
    shorthand = resource

    from metadrive import drivers
    ENSURE_SITES()
    # finding driver by default domain

    # 1. Getting default domain
    from metadrive._selenium import get_drive
    drive = get_drive(headless=True)
    if not resource.startswith('http'):
        resource = 'http://' + resource
    drive.get(resource)
    url = drive.current_url
    drive.quit()
    default_domain = urlparse(url).hostname

    # 2. Checking for driver with it.
    index = drivers.index()
    results = list(filter(lambda x: x['domain']==default_domain, index))

    if not results:
        print("No drivers found for {}.".format(resource))
        print("Drivers currently available for domains:\n")
        for item in index:
            if item.get('domain'):
                print(' - {} [{}]'.format(item.get('domain'), item.get('package')))

        print("\n You can create a new driver by publishing a PyPI package,\n\
that ends with _driver or -driver, and has __site_url__ variable\n\
specified its __init__.py file. More details on creating a driver\n\
are in https://github.com/wefindx/metadrive/blob/master/docs/DRIVER_PACKAGE_STRUCTURE.md\n\
and https://github.com/wefindx/metadrive/blob/master/docs/RULES.md files,\n\
as well as look at examples on https://github.com/drivernet (such as\n\
https://github.com/drivernet/halfbakery-driver)")
        return

    first_driver = results[0]

    try:
        import pkg_resources
        package_version = pkg_resources.require(first_driver.get('package'))[0].version
    except:
        # print("The package not yet installed. Latest package found.")
        package_version = first_driver.get('info')['version']

    print("-================================================-\n[*] using: [PyPI:{packname}=={version}]".format(
        packname=first_driver.get('package'),
        version=package_version #'>'+first_driver.get('info')['version']
        ),
    )

    if mountpoint is None:
        mountpoint = os.path.join(SITES_DIR, shorthand)
        # print("Assuming mount point: {}".format(mountpoint))

    package = utils.ensure_driver_installed(
        '{packman}:{packname}'.format(
            packman=first_driver.get('type'),
            packname=first_driver.get('package')
        )
    )

    module = __import__(package)
    api = importlib.import_module('{}.api'.format(package))

    # print('\nTop level methods:\n')
    # for met in dir(module):
    #     if not met.startswith('__') and met not in ['api']:
    #         print(' - ', met)
    #

    # print('\nAvailable api classes:\n')
    # for cls in dir(api):
    #     if cls[0].isupper() and not cls.startswith('_') and cls not in ['Dict']:
    #         print(' - ', cls)
    #

    drive_name = 'default' #input("Enter the name of drive [default]: ") or 'default'

    # drive = get_drive(
    #     profile=profile,
    #     recreate_profile=recreate_profile,
    #     proxies=proxies)

    if user is None:
        drive = metadrive.drives.get(package.replace('_', '-'), interactive=True)
        drive_name = drive.drive_id.rsplit(':', 1)[-1]
    else:
        drive_name = user
        drive_fullname = '{package}:{drive}'.format(
            package=package.replace('_', '-'),
            drive=drive_name
        )
        drive = metadrive.drives.get(drive_fullname, interactive=False)


    mountpoint = '{}:{}'.format(mountpoint, drive_name)
    if not os.path.exists(mountpoint):
        os.makedirs(mountpoint)

    drive_fullname = '{package}:{drive}'.format(
        package=package.replace('_', '-'),
        drive=drive_name
    )

    # drive == metadrive.drives.get(drive_fullname)
    savedir = os.path.join(metadrive.config.DATA_DIR, drive_fullname)

    if user is None:
        print("Pass '--user {}' next time, to reuse the session.".format(drive_name))

    def sync():
        print("[*] mount: {}\n-================================================-".format(mountpoint))
        import inspect
        if 'period' in inspect.getfullargspec(module._harvest).args:
            module._harvest(drive=drive, period=period)
        else:
            module._harvest(drive=drive)

    from multiprocessing import Process
    syncer = Process( target=sync )
    syncer.daemon = True
    syncer.start()

    mount(savedir, mountpoint)
    syncer.terminate()
