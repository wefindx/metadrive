__site_url__ = 'http://www.halfbakery.com'
__base_url__ = 'http://www.halfbakery.com'

import os
import requests
import feedparser
import metawiki

from metadrive import utils

from dateutil.parser import parse as dateparse
from datetime import timezone

def login(username=None, password=None):
    '''
    Creates, serializes and saves session
    ( utils.save_session_data )
    '''

    session = requests.Session()
    session.metaname = utils.get_metaname('halfbakery')

    session_data = utils.load_session_data(
        namespace='halfbakery')

    if session_data:
        session.cookies.update(
            requests.utils.cookiejar_from_dict(
                session_data))
        return session

    if not username and password:
        credential = utils.get_or_ask_credentials(
            namespace='halfbakery',
            variables=['username', 'password'])

        username = credential['username']
        password = credential['password']

    if session.get('http://www.halfbakery.com/lr/').ok:
        signin = session.get('http://www.halfbakery.com/lr/',
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

def get(url, session=None):
    '''
    -> Download a single item content.
    In Halfbakery, that gives full text with comments.
    '''
    session.get(url)

def search(
        query=None,
        session=None,
        page_size=100,
        offset=0,
        limit=None,
        get_detail=False):
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

            ### Conform to the result to record format '::mindey/topic#halfbakery' ###

            record = {}
            created, updated = result['dc_coverage'].split(' - ')
            created_utc = dateparse(created).astimezone(timezone.utc).isoformat()
            updated_utc = dateparse(updated).astimezone(timezone.utc).isoformat()

            record['author'] = {
                'date': created_utc,
                'userlink': 'http://www.halfbakery.com/user/{}'.format(result['author'].replace(' ', '_20')),
                'username': result['author'],
                'last_modified': updated_utc
            }
            record['category'] = result['tags'][0]['term']

            def title_vote_splitter(title_info):

                title = title_info.rsplit(' (', 1)[0]

                meal_votes = title_info.rsplit(' (', 1)[-1][:-1]
                meal, votes = meal_votes.split(': ')
                meal = float(meal)

                if ',' in votes:
                    pos, neg = votes.split(', ')
                else:
                    if votes.startswith('+'):
                        pos, neg = int(votes[1:]), 0
                    elif votes.startswith('-'):
                        pos, neg = 0, int(votes[1:])
                    else:
                        pos, neg = 0, 0

                return {'title': title,
                        'meal': meal,
                        'votes': {'positive': pos, 'negative': neg}}

            title_details = title_vote_splitter(result['title'])
            record['title'] = title_details['title']
            record['votes'] = title_details['votes']
            record['meal'] = title_details['meal']

            if session:
                record['+'] = metawiki.name_to_url(session.metaname)
            record['-'] = result['id']

            #
            # if get_detail=True, call the get()
            # asynchronously in parallel.
            #
            yield record

        if len(results) < page_size:
            break

        offset += page_size

        if limit:
            if offset >= limit:
                break

def generate(query=None, limit=None):
    '''
    Combines login, get, search into a procudure sufficient to generate full-fledged items.
    '''

    if input('Do you want to login to Halfbakery? [y/N] ') in ['y', 'Y']:
        session = login()
    else:
        session = None

    if input('Do you want to get detail of each search result? (In Halfbakery, that means full text of each post, and comments. Takes much time. [y/N] ') in ['y', 'Y']:
        get_detail = True
    else:
        get_detail = False


    for item in search(
            query=query,
            session=session,
            get_detail=get_detail,
            limit=limit):

        yield item
