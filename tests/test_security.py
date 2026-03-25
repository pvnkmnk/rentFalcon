import pytest
from unittest.mock import MagicMock, patch
import re

# Mock ScraperManager BEFORE importing app
with patch('scrapers.scraper_manager.ScraperManager') as MockManager:
    mock_instance = MockManager.return_value
    mock_instance.search_all.return_value = {
        "listings": [],
        "stats": {
            "total_listings": 0,
            "unique_listings": 0,
            "duplicates_removed": 0,
            "scrapers_succeeded": 0,
            "scrapers_failed": 0,
            "execution_time": 0,
            "by_source": {},
        },
        "errors": {}
    }
    mock_instance.get_available_scrapers.return_value = []
    mock_instance.get_enabled_scrapers.return_value = []
    from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = True
    app.config['SECRET_KEY'] = 'test-secret'
    with app.test_client() as client:
        yield client

def test_index_post_no_csrf_rejected(client):
    """
    Test that POST to index is REJECTED without CSRF token
    """
    response = client.post('/', data={
        'location': 'newmarket',
        'price_min': '1000',
        'price_max': '2000'
    })

    # CSRFProtect returns 400 Bad Request when token is missing
    assert response.status_code == 400

def test_api_search_csrf_exempt(client):
    """
    Test that API search is EXEMPT from CSRF protection
    """
    response = client.post('/api/search', json={
        'location': 'newmarket'
    })

    assert response.status_code == 200

def test_index_get_contains_csrf_token(client):
    """
    Test that the index page contains a CSRF token in the form
    """
    response = client.get('/')
    assert response.status_code == 200
    assert b'name="csrf_token"' in response.data
    assert b'value="' in response.data
