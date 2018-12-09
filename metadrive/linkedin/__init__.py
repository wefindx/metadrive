__site_url__ = 'https://www.linkedin.com'
__base_url__ = 'https://api.linkedin.com'

import time
import bs4
from metadrive import utils
import datetime
import metawiki

from _selenium import get_driver

def login(username=None, password=None, profile=None, recreate_profile=False):

    # session_data = utils.load_session_data(
    #     namespace='linkedin')
    #
    # if session_data:
    #     # session is a driver
    #     # session = load(session_data)
    #     # return session
    #     pass

    driver = get_driver(recreate_profile=recreate_profile)
    driver.get('https://www.linkedin.com/')
    soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')

    if soup.find('div', {'class': 'core-rail'}):
        driver.metaname = utils.get_metaname('linkedin')
        return driver

    if not (username and password):
        credential = utils.get_or_ask_credentials(
            namespace='linkedin',
            variables=['username', 'password'], ask_refresh=True)

        username = credential['username']
        password = credential['password']

    user_field = soup.find('input', {'class': 'login-email'})
    pass_field = soup.find('input', {'class': 'login-password'})

    if user_field and pass_field:

        driver.find_element_by_class_name('login-email').send_keys(username)
        driver.find_element_by_class_name('login-password').send_keys(password)
        driver.find_element_by_id('login-submit').click()
        soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')

        if soup.find('div', {'id': 'error-for-password'}):
            raise Exception("Incorrect password. Try to relogin.")

        if soup.find('button', {'class': 'artdeco-dismiss'}):
            'Removing the notification about cookies.'
            driver.find_element_by_class_name('artdeco-dismiss').click()

    soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')

    if soup.find('div', {'class': 'core-rail'}):
        return driver
    else:
        raise Exception("Something wrong, the site does not have timeline (core-rail).")


def generate(limit=None, close_after_execution=True):
    '''
    Scrolls down for a little while, repeats it and yields results.
    # {
    # 'url': 'https://www.linkedin.com/feed/update/urn:li:activity:6470051339450740737', 'date': None, 'body': None, 'comments': [], 'mentioned_by': 'https://www.linkedin.com/in/ACoAAAUSGH8BeP-kg121PCBxwTv3SpcLzwLOQm0/', 'shared_by': 'Antoinette Weibel', 'logged': '2018-11-19T10:02:18.453122'}
    '''

    driver = login()

    while True:

        soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')
        posts_placeholder = soup.find('div', {'class': 'core-rail'})
        posts = posts_placeholder.find_all('div', {'class': 'relative ember-view'})

        count = 0

        for i, post in enumerate(posts):

            url = 'https://www.linkedin.com/feed/update/'+post.attrs['data-id']

            shared_by = post.find('div', {'class': 'presence-entity'})
            if shared_by:
                shared_by = shared_by.find('div', {'class': 'ivm-view-attr__img--centered'})
                if shared_by:
                    shared_by = shared_by.text
                    if shared_by:
                        shared_by = shared_by.strip()

            text = post.find('div', {'class': 'feed-shared-text'})
            if isinstance(text, str):
                text = text.strip()
            else:
                text = None

            mentioned_by = post.find('a', {'class': 'feed-shared-text-view__mention'})
            if mentioned_by:
                profile_path = mentioned_by.attrs.get('href')
                if profile_path:
                    mentioned_by = 'https://www.linkedin.com'+profile_path

            # comments =
            # media =

            item = {
                'url': url,
                'date': None,
                'body': text,
                'comments': [],
                'mentioned_by': mentioned_by,
                'shared_by': shared_by,
                'logged': datetime.datetime.utcnow().isoformat(),
                '-': url,
                '+': metawiki.name_to_url(driver.metaname),
                '*': metawiki.name_to_url('::mindey/topic#linkedin')
            }

            count += 1
            yield item

            if limit:
                if count >= limit:
                    break

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
