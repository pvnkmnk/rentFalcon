import pytest
import os
from unittest.mock import patch, MagicMock
from app import app

@pytest.fixture
def client():
    # Set required environment variables for config
    os.environ['SECRET_KEY'] = 'test-key'
    os.environ['FLASK_ENV'] = 'development'

    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = True
    app.config['SECRET_KEY'] = 'test-key'

    with app.test_client() as client:
        yield client

@patch('app.manager.search_all')
def test_csrf_protection_on_index(mock_search, client):
    """
    Verify that the index route now REJECTS POST requests without a CSRF token.
    """
    # Attempt POST without any CSRF token
    response = client.post('/', data={'location': 'ottawa'})

    # It should fail with 400 Bad Request (CSRF token missing)
    assert response.status_code == 400
    assert b"The CSRF token is missing" in response.data or b"Bad Request" in response.data

@patch('app.manager.search_all')
def test_csrf_protection_success_with_token(mock_search, client):
    """
    Verify that the index route ACCEPTS POST requests with a valid CSRF token.
    """
    mock_search.return_value = {
        "listings": [],
        "stats": {
            "unique_listings": 0,
            "scrapers_succeeded": 1,
            "duplicates_removed": 0,
            "execution_time": 0.1,
            "by_source": {"test": 0}
        },
        "errors": {}
    }

    # 1. Get the page to set the session and get a token
    response = client.get('/')
    assert response.status_code == 200

    # Extract CSRF token from the form (using a simple search or a parser)
    import re
    html = response.data.decode()
    match = re.search(r'name="csrf_token" value="([^"]+)"', html)
    assert match is not None
    csrf_token = match.group(1)

    # 2. POST with the token
    response = client.post('/', data={
        'location': 'ottawa',
        'csrf_token': csrf_token
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Rental Listings" in response.data or b"Listings Found" in response.data

@patch('app.manager.search_all')
def test_api_search_exempt_from_csrf(mock_search, client):
    """
    Verify that the API endpoint is exempt from CSRF protection.
    """
    mock_search.return_value = {"listings": [], "stats": {}, "errors": {}}

    # Attempt POST without CSRF token
    response = client.post('/api/search', json={'location': 'ottawa'})

    # It should still work
    assert response.status_code == 200
