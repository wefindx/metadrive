import bs4
from metadrive._requests import get_session
from metadrive._selenium import get_drive

def get_drive():
    # drive.caller_module = inspect.getmodule(inspect.currentframe().f_back)
    raise NotImplemented

def get_soup(url, session=None, use='requests', proxies=None, update_headers=None):
    if use == 'requests':
        if session is None:
            session = get_session()

        if update_headers is not None:
            session.headers.update(update_headers)

        response = session.get(url, proxies=proxies)
        if response.ok:
            data = response.content
        else:
            data = None
            raise Exception("Response was wrong, error ({}): {}".format(
                response.status_code, data))
    elif use == 'selenium':
        if session is None:
            session = get_drive(headless=True)
            session.get(url)
            data = session.page_source
            session.quit()
        else:
            session.get(url)
            data = session.page_source

    soup = bs4.BeautifulSoup(data, 'html.parser')
    return soup

def dictify_ul(ul):
    '''
    Source:
    https://stackoverflow.com/questions/17850121/parsing-nested-html-list-with-beautifulsoup
    '''
    result = {}
    for li in ul.find_all("li", recursive=False):
        key = next(li.stripped_strings)
        ul = li.find("ul")
        if ul:
            result[key] = dictify_ul(ul)
        else:
            result[key] = None
    return result
