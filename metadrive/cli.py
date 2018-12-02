import click
import json
import metadrive
from metaform import slug
from metawiki import name_to_url
import os
from urllib.parse import urlparse

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

    for item in metadrive.read(resource, limit=limit):
        item['*'] = resource

        if db:
            ID = item['-']
            # Writing to database:
            if dbinfo.scheme == 'mongodb':
                print('DB:INFO:', item['-'])
                db[table].update_one(
                    {'-': ID}, {'$set': item}, upsert=True)

        else:
            s = slug(item['-'])
            c = item['-'].rsplit('#')[-1][:7]
            ID = s[:FILENAME_LENGTH_LIMIT-12]+'#{}'.format(c)+'.json'
            # Writing to file:

            if output:
                ID = os.path.join(output, ID)

            with open(ID, 'w') as f:
                print('FILE:INFO:', item['-'])
                f.write(json.dumps(item))
