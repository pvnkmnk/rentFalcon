import pytest
from app import app
from unittest.mock import patch

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    with app.test_client() as client:
        yield client

@patch('app.manager.search_all')
def test_csrf_protection_on_search(mock_search, client):
    """Test that POST to / is protected by CSRF"""
    mock_search.return_value = {
        "listings": [],
        "stats": {
            "unique_listings": 0,
            "scrapers_succeeded": 0,
            "duplicates_removed": 0,
            "execution_time": 0,
            "by_source": {}
        },
        "errors": {}
    }

    # Attempting a POST without CSRF token should fail with 400 Bad Request
    response = client.post('/', data={'location': 'ottawa'})
    assert response.status_code == 400
    assert b"The CSRF token is missing" in response.data or b"Bad Request" in response.data

@patch('app.manager.search_all')
def test_api_search_csrf_exempt(mock_search, client):
    """Test if /api/search is CSRF exempt"""
    mock_search.return_value = {
        "listings": [],
        "stats": {},
        "errors": {},
        "timestamp": "2023-01-01"
    }

    # POST to /api/search should NOT fail with 400 even without CSRF token
    response = client.post('/api/search', json={'location': 'ottawa'})
    assert response.status_code == 200
