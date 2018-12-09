__site_url__ = 'https://inf.li'
__base_url__ = 'https://wefindx.io'

# Thinking - we should make the inf.li functionality only, as API service.

import apiage

def generate(limit=None):
    for item in apiage.gen('https://inf.wefindx.com/topics/', silent=True):
        yield item
