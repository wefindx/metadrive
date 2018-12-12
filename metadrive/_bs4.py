import bs4
from metadrive._requests import get_session
from metadrive._selenium import get_driver

def get_soup(url, session=None, use='requests'):
    if use == 'requests':
        if session is None:
            session = get_session()

        response = session.get(url)
        if response.ok:
            data = response.content
        else:
            data = None
            raise Exception("Response was wrong, error ({}): {}".format(
                response.status_code, data))
    elif use == 'selenium':
        if session is None:
            session = get_driver(headless=True)
        session.get(url)
        data = session.page_source
        session.quit()

    soup = bs4.BeautifulSoup(data, 'html.parser')
    return soup
