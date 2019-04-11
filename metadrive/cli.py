import click
import json
import metadrive
from typology.utils import slug
from metawiki import name_to_url
import os
from urllib.parse import urlparse
from metadrive.config import (
    API_HOST,
    API_PORT,
    CONSOLE_HOST,
    CONSOLE_PORT,
)

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

