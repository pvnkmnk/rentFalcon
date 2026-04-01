import pytest
from app import app
from flask import url_for

@pytest.fixture
def client():
    app.config['TESTING'] = True
    # Ensure WT_CSRF_ENABLED is True for security tests
    app.config['WTF_CSRF_ENABLED'] = True
    app.config['DEBUG'] = False
    with app.test_client() as client:
        yield client

def test_index_post_no_csrf(client):
    """POST to index without CSRF token should fail with 400"""
    response = client.post('/', data={'location': 'ottawa'})
    assert response.status_code == 400

def test_api_search_no_csrf(client, mocker):
    """POST to /api/search without CSRF token should SUCCEED because it is exempted"""
    # Mock manager.search_all to avoid actual scraping
    mock_search = mocker.patch('app.manager.search_all')
    mock_search.return_value = {'listings': [], 'stats': {}, 'errors': {}}

    response = client.post('/api/search', json={'location': 'ottawa'})
    # It should not be 400. It might be 200 if valid or 500 if mock fails, but not 400 CSRF error.
    assert response.status_code == 200

def test_index_get_has_csrf_token(client):
    """GET index should contain the CSRF token in the form"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'name="csrf_token"' in response.data
    assert b'value="' in response.data
