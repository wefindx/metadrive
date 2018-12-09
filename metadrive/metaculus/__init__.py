__site_url__ = 'https://www.metaculus.com'
__base_url__ = 'https://www.metaculus.com/api2'

import apiage
from .utils import clean_em


def generate(query=None, limit=None):

    for item in apiage.gen(
        'https://www.metaculus.com/api2/questions/',
            limit=limit, silent=True):
        item = clean_em(item)
        item['-'] = item['url']
        yield item


