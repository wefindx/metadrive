import apiage

def generate(query=None, limit=None):

    return apiage.gen(
        'https://www.metaculus.com/api2/questions/',
        limit=limit)

