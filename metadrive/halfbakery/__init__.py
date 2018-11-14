import os
import requests
import feedparser
import config

from metaform import get_schema

def login(username=None, password=None):

    if 'halfbakery.session' in os.listdir(config.DEFAULT_LOCATION):
        # read session #
        pass
    else:
        # use known password #
        if not (username and password):

            try:
                credentials = metaform.get_schema(
                    '-:{gituser}/metadrive/halfbakery.md#main'.format(
                        config.GITHUB_USER))
            except:
                credentials = None

            if credentials:
                # decrypt #
                pass
            else:

            in ['-repo']:
                print('Log-in to Halfbakery:')
            if not username:
                username = input('username = ')
            if not password:
                password = input('password = ')

        # logging in

        print('logging in')
    #
    # else:
    #     print('Found `halfbakery.session` in ~/.metadrive, using existing session.')



    print('saving login token...')
    print("creating - repository, if doesn't exist")
    print('saving login session...')
    save_login = input('Do you want to encrypt and save password on github? [Y/n] ')
    pass

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
