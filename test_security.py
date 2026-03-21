import pytest
from app import app
import os
@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = True
    app.config['SECRET_KEY'] = 'test-key'
    with app.test_client() as client:
        yield client
def test_index_post_fails_without_csrf(client):
    response = client.post('/', data={'location': 'ottawa'})
    assert response.status_code == 400
    assert b'The CSRF token is missing' in response.data
def test_api_search_succeeds_without_csrf(client):
    from app import manager
    original = manager.search_all
    manager.search_all = lambda l, mi, ma: {"listings": [], "stats": {"scrapers_succeeded": 0, "execution_time": 0}, "errors": {}}
    response = client.post('/api/search', json={'location': 'ottawa'}, content_type='application/json')
    manager.search_all = original
    assert response.status_code == 200
def test_index_get_succeeds(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'csrf_token' in response.data
