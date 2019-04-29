from metadrive.tests.conftest import client

def test_sanity():
    assert 1 == 1

def test_root(client):
    response = client.get('http://0.0.0.0:8000')
    assert response.text.startswith('<!doctype ht')

def test_drivers(client):
    response = client.get('http://0.0.0.0:8000/drivers')
    assert type(response.json()) == list

def test_drives(client):
    response = client.get('http://0.0.0.0:8000/drives')
    assert type(response.json()) == list
