import requests

def get_drive():
    raise NotImplemented

def get_session(*args, **kwargs):
    return requests.Session(*args, **kwargs)
