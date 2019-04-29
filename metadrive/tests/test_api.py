from metadrive.tests.conftest import client

def test_sanity():
    assert 1 == 1

def test_root(client):
    response = client.get('http://0.0.0.0:8000')
    assert response.text.startswith('<!doctype ht')

