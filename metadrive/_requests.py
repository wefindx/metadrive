import requests

def get_session(*args, **kwargs):
    return requests.Session(*args, **kwargs)
