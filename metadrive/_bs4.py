import bs4
from metadrive._requests import get_session

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

        soup = bs4.BeautifulSoup(data, 'html.parser')
        return soup
