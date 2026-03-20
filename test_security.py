
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    with app.test_client() as client:
        yield client

def test_csrf_protection_on_index(client):
    """Test that POST to / fails without CSRF token"""
    response = client.post('/', data={'location': 'newmarket'})
    assert response.status_code == 400
    assert b"The CSRF token is missing" in response.data

def test_csrf_protection_exempt_api(client):
    """Test that POST to /api/search works without CSRF token"""
    # Mocking the manager.search_all to avoid actual scraping during test
    from unittest.mock import patch
    with patch('app.manager.search_all') as mock_search:
        mock_search.return_value = {
            "listings": [],
            "stats": {"unique_listings": 0, "scrapers_succeeded": 0, "execution_time": 0, "duplicates_removed": 0, "by_source": {}},
            "errors": {}
        }
        response = client.post('/api/search',
                             json={'location': 'newmarket'},
                             content_type='application/json')
        assert response.status_code == 200
