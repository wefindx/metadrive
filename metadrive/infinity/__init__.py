import apiage

def generate(limit=None):
    for item in apiage.gen('https://inf.wefindx.com/topics/', silent=True):
        yield item
