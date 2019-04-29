import pytest
from starlette.config import environ
from starlette.testclient import TestClient

environ['TESTING'] = 'TRUE'

from metadrive.api import app

@pytest.fixture()
def client():
    with TestClient(app) as test_client:
        yield test_client
