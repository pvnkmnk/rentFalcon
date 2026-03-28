import pytest
from app import app
from flask_wtf.csrf import generate_csrf
import re

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = True
    app.config['SECRET_KEY'] = 'test-key'
    with app.test_client() as client:
        yield client

def test_index_post_without_csrf(client):
    """Test that POST request to index fails without CSRF token"""
    response = client.post('/', data={'location': 'newmarket'})
    assert response.status_code == 400

def test_index_post_with_csrf(client):
    """Test that POST request to index succeeds with CSRF token"""
    # First, get the main page to get the CSRF token in session
    response = client.get('/')
    assert response.status_code == 200

    # Extract CSRF token from HTML
    html = response.get_data(as_text=True)
    csrf_token_match = re.search(r'name="csrf_token" value="([^"]+)"', html)
    assert csrf_token_match
    csrf_token = csrf_token_match.group(1)

    # Send POST with the token
    response = client.post('/', data={
        'location': 'newmarket',
        'csrf_token': csrf_token
    })

    # Should get past CSRF check.
    # It might result in 200 (if search completes) or something else if scraper fails.
    # 400 would be a CSRF failure.
    assert response.status_code != 400

def test_api_search_exempt_csrf(client):
    """Test that API endpoint is exempt from CSRF"""
    response = client.post('/api/search', json={'location': 'newmarket'})
    # It should not return 400 CSRF error.
    assert response.status_code != 400
