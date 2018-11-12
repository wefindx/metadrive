import requests
import feedparser

def login(username, password):
    '''
    -> store session locally in '~/.metaform'
    -> store encrypted credentials with data in github, to use as link.
    '''
    print('performing login...')
    pass

def sync_one(url):
    '''
    -> Download a single item content with comments.
    '''
    pass

def sync_all(limit=100, offset=0, sync_comments=False):
    '''
    -> Download all titles, descriptions and dates.
    -> Create if not exists, update if exists. (call sync_one if updated)
    -> produce (yield) items with *, +, -.
    '''
    feed_url = 'http://www.halfbakery.com/lr/view/fxc=230:s=R:d=iwqhvroc:do={offset}:dn={limit}:ds=A:n=tiny:t=halfbakery'.format(
        limit=limit,
        offset=offset
    )

    feedparser.parse(feed_url)

    print(feed_url)


def harvest():

    authenticate = input('Do you want to login and bind encrypted login info? [y/N] ')

    if authenticate in ['y', 'Y']:
        login()

    for item in sync_all():
        yield item
