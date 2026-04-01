import pytest
from app import app, csrf
import json
import re

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    with app.test_client() as client:
        yield client

def test_index_post_no_csrf(client):
    """Test that POST / fails without CSRF token"""
    response = client.post('/', data={'location': 'newmarket'})
    assert response.status_code == 400

def test_index_post_with_csrf(client):
    """Test that POST / works with a valid CSRF token"""
    # 1. GET the page to get the CSRF token in the session
    get_response = client.get('/')
    assert get_response.status_code == 200

    # 2. Extract CSRF token from the HTML response
    html = get_response.get_data(as_text=True)
    match = re.search(r'name="csrf_token" value="([^"]+)"', html)
    assert match is not None
    csrf_token = match.group(1)

    # 3. POST with the token
    # We mock the manager.search_all if we want to avoid actual scraping,
    # but for a security test, we just check if it bypasses CSRF protection.
    # Since we can't easily mock the manager here without more setup,
    # let's just check if it gets past the CSRF check (i.e. status != 400)
    response = client.post('/', data={
        'location': 'newmarket',
        'csrf_token': csrf_token
    })

    # It should not be 400.
    # It might be 200 (if search succeeds or error is caught and template rendered)
    assert response.status_code != 400

def test_api_search_no_csrf(client):
    """Test that POST /api/search works WITHOUT CSRF token (it is exempted)"""
    response = client.post('/api/search',
                          data=json.dumps({'location': 'newmarket'}),
                          content_type='application/json')

    # It should NOT be 400 (CSRF error).
    assert response.status_code != 400
