import pytest
from app import app as flask_app

@pytest.fixture
def client():
    flask_app.testing = True
    with flask_app.test_client() as client:
        yield client

def test_root_returns_200(client):
    resp = client.get('/')
    assert resp.status_code == 200

def test_healthz_returns_200(client):
    resp = client.get('/healthz')
    assert resp.status_code == 200

def test_root_contains_hello(client):
    resp = client.get('/')
    assert "Hello" in resp.get_data(as_text=True)