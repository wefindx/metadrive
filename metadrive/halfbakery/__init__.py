import os
import requests
import feedparser

from metadrive import (
    config,
    utils
)


def login(username=None, password=None):

    session = requests.Session()

    session_data = utils.load_session_data(
        namespace='halfbakery')

    if session_data:
        session.cookies.update(
            requests.utils.cookiejar_from_dict(
                session_data))
        return session

    credential = utils.ensure_credentials(
        namespace='halfbakery',
        variables=['username', 'password'])

    username = credential['username']
    password = credential['password']

    if session.get(
            'http://www.halfbakery.com/lr/').ok:
        signin = session.get(
            'http://www.halfbakery.com/lr/',
             params={
                 'username': username,
                 'password': password,
                 'login': 'login'})

        if signin.ok:
            utils.save_session_data(
                'halfbakery',
                requests.utils.dict_from_cookiejar(
                    session.cookies))

            return session
        else:
            raise Exception(
                'Could not signin: {}'.format(
                    signin.status_code))
    else:
        raise Exception(
            'Failed to open Halfbakery: {}'.format(
                signin.status_code))

def get(url):
    '''
    -> Download a single item content with comments.
    '''
    pass

def search(page_size=100, offset=0, limit=None, get_comments=False):
    '''
    -> Download all titles, descriptions and dates.
    -> Create if not exists, update if exists. (call sync_one if updated)
    -> produce (yield) items with *, +, -.
    '''

    feed_url = 'http://www.halfbakery.com/lr/view/fxc=230:s=R:d=iwqhvroc:do={offset}:dn={page_size}:ds=A:n=tiny:t=halfbakery'

    while True:

        results = feedparser.parse(feed_url.format(
            page_size=page_size,
            offset=offset
        ))['entries']

        for result in results:
            result['-'] = result['id']
            yield result

        if len(results) < page_size:
            break

        offset += page_size

        if limit:
            if offset >= limit:
                break


def generate(limit=None):
    '''
    Combines login, get, search into a procudure sufficient to generate full-fledged items.
    '''

    authenticate = input('Do you want to login to Halfbakery? [y/N] ')

    if authenticate in ['y', 'Y']:
        login()

    complete = input('Do you want to synchronize comments? Takes much time. [y/N] ')

    if complete in ['y', 'Y']:
        complete = True
    else:
        complete = False


    for item in search(get_comments=complete, limit=limit):
        yield item
