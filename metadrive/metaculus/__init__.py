import apiage

def generate(query=None, limit=None):

    for item in apiage.gen(
        'https://www.metaculus.com/api2/questions/',
            limit=limit, silent=True):
        item['-'] = item['url']
        yield item
