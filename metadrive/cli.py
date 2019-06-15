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
    API_HOST,
    API_PORT,
    CONSOLE_HOST,
    CONSOLE_PORT,
    ENSURE_SITES,
    SITES_DIR,
)
from metadrive.mnt import mount

@click.command()
def console():
    from metadrive import api
    host = CONSOLE_HOST
    port = CONSOLE_PORT

    def serve():
        api.uvicorn.run(
            api.app,
            host=host,
            port=port,
            log_level='error'
        )

    from multiprocessing import Process
    server = Process( target=serve )
    server.daemon = True
    server.start()

    from metadrive import console
    console.repl(host=host, port=port)
    server.terminate()

@click.command()
def provide():
    # https://www.starlette.io/applications/
    from metadrive import api
    api.uvicorn.run(
        api.app, host=API_HOST, port=API_PORT, log_level='info')


@click.command()
@click.option('--ui', required=False, type=str, help='Save results to specified database.')
def consume(ui=None):
    # https://www.starlette.io/testclient/
    # from metadrive import api
    # from starlette.testclient import TestClient
    #
    # client = TestClient(api.app)
    # with client.websocket_connect('/ws') as websocket:
    #     data = websocket.receive_text()
    #
    # print(data)
    from metadrive import api
    host = CONSOLE_HOST
    port = CONSOLE_PORT

    def serve():
        api.uvicorn.run(
            api.app,
            host=host,
            port=port,
            log_level='error'
        )

    from multiprocessing import Process
    server = Process( target=serve )
    server.daemon = True
    server.start()

    if ui is None:
        # if ui == 'react'
        from metadrive.ui import ReactJS
        ReactJS().start()
    else:
        # using ncurses
        from metadrive.ui import NCurses
        NCurses().run()

    server.terminate()


# Cause ecryptfs supports max 143 chars.
FILENAME_LENGTH_LIMIT = 143

@click.command()
@click.help_option('-h')
@click.argument('resource', required=True, metavar='<resource>')
@click.option('-l', '--limit', required=False, type=int, help='Limit to the number of records to download.')
@click.option('-o', '--output', required=False, type=str, help='Save results as files to specified folder.')
@click.option('--db', required=False, type=str, help='Save results to specified database.')
def harvest(resource, limit=None, output=None, db=None):
    """Pulls data from a resource, and saves it in data items with metaformat metadata.

    $ harvest <resource>

    $ harvest <resource> --db mongodb://localhost/<db-name>/<collection-name>
    """
    if db:
        # Creating db connection
        dbinfo = urlparse(db)

        dbname_table = [o for o in dbinfo.path.split('/') if o]

        if len(dbname_table) != 2:
            raise Exception(
                'The database path must contain name ' +
                'of the database and table (collection) ' +
                'split by /. Got path: {}'.fromat(dbinfo.path))

        dbname, table = dbname_table

        if dbinfo.scheme == 'mongodb':

            import pymongo

            if len(dbinfo.netloc.split(':')) == 2:
                dbinfo = dbinfo._replace(netloc=dbinfo.netloc+':27017')

            db = getattr(pymongo.MongoClient(
                dbinfo.scheme+'://'+dbinfo.netloc), dbname)

        else:
            raise Exception(
                'Unknown scheme, got: {}.'.format(dbinfo.scheme))

    if limit:
        limit = int(limit)
    else:
        limit = None

    if not resource.startswith('http'):
        resource = name_to_url(resource)

    for n, item in enumerate(metadrive.read(resource, limit=limit)):
        item['*'] = resource

        if db:
            ID = item.get('-')
            if ID is None:
                raise Exception("The crawler (driver) emitted items must have '-' key containing URLs of items.")
            # Writing to database:
            if dbinfo.scheme == 'mongodb':
                print('DB:INFO:', item['-'])
                db[table].update_one(
                    {'-': ID}, {'$set': item}, upsert=True)

        else:
            ID = item.get('-')
            if ID is None:
                if item.get('url') is not None:
                    item['-'] = item.get('url')
                    ID = item.get('url')
                else:
                    raise Exception("The crawler (driver) emitted items must have '-' (or 'url') key containing URLs of items.")
            s = slug(ID)
            # c = slug(item['-'].rsplit('#')[0][-7:])
            ID = s[:FILENAME_LENGTH_LIMIT-12]+'#{}'.format(n)+'.json'
            # Writing to file:

            if output:
                ID = os.path.join(output, ID)

            if output is not None:
                if not os.path.exists(output):
                    os.makedirs(output)

            with open(ID, 'w') as f:
                print('FILE:INFO:', item['-'])
                f.write(json.dumps(item))


@click.command()
@click.argument('resource', required=True, metavar='<resource>')
@click.argument('mountpoint', required=False, metavar='<mountpoint>')
def connect(resource, mountpoint=None):
    """
    Mounts interactive data from a resource as a filesystem to OS.
    $ connnect <resource> [location]
    """
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

    print("\nDriver found: {packname}=={version}".format(
        packname=first_driver.get('package'),
        version=first_driver.get('info')['version'])
    )

    if mountpoint is None:
        mountpoint = os.path.join(SITES_DIR, shorthand)
        print("Assuming mount point: {}".format(mountpoint))

    package = utils.ensure_driver_installed(
        '{packman}:{packname}'.format(
            packman=first_driver.get('type'),
            packname=first_driver.get('package')
        )
    )

    module = __import__(package)
    api = importlib.import_module('{}.api'.format(package))

    print('\nTop level methods:\n')
    for met in dir(module):
        if not met.startswith('__') and met not in ['api']:
            print(' - ', met)

    print('\nAvailable api classes:\n')
    for cls in dir(api):
        if cls[0].isupper() and not cls.startswith('_') and cls not in ['Dict']:
            print(' - ', cls)


    print('\n\nNow:')
    print('\nStill, need to create drive and log-in. (Need to choose drive name, which would return data path)\n')

    print('\n1. _harvest should orchestrate synchronization using (cls)._sync() methods...')
    print('\n2. we should use () ...')

    drive_name = 'default' #input("Enter the name of drive [default]: ") or 'default'

    mountpoint = '{}:{}'.format(mountpoint, drive_name)
    if not os.path.exists(mountpoint):
        os.makedirs(mountpoint)

    drive_fullname = '{package}:{drive}'.format(
        package=package.replace('_', '-'),
        drive=drive_name
    )

    # drive == metadrive.drives.get(drive_fullname)
    savedir = os.path.join(metadrive.config.DATA_DIR, drive_fullname)

    # drive = get_drive(
    #     profile=profile,
    #     recreate_profile=recreate_profile,
    #     proxies=proxies)

    def sync():
        print("{} -> {}".format(shorthand, mountpoint))
        drive = metadrive.drives.get(drive_fullname)
        # drive = module._login(profile=drive_name) # maybe in the future we should change _login(profile->drive_name)
        module._harvest(drive=drive)

    from multiprocessing import Process
    syncer = Process( target=sync )
    syncer.daemon = True
    syncer.start()

    mount(savedir, mountpoint)
    syncer.terminate()
