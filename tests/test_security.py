import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = True
    # Ensure SECRET_KEY is set for tests
    if not app.config.get('SECRET_KEY'):
        app.config['SECRET_KEY'] = 'test-key'

    with app.test_client() as client:
        yield client

def test_index_post_no_csrf(client):
    """Test that POST to / fails without CSRF token"""
    response = client.post('/', data={'location': 'newmarket'})
    assert response.status_code == 400
    # Flask-WTF usually returns 400 when CSRF is missing

def test_api_search_post_no_csrf(client):
    """Test that POST to /api/search succeeds without CSRF token (exempted)"""
    # Mock manager.search_all to avoid actual scraping
    from unittest.mock import patch
    with patch('app.manager.search_all') as mock_search:
        mock_search.return_value = {
            "listings": [],
            "stats": {"scrapers_succeeded": 0, "execution_time": 0},
            "errors": {}
        }
        response = client.post('/api/search',
                             json={'location': 'newmarket'},
                             content_type='application/json')
        assert response.status_code == 200

def test_health_get(client):
    """Test that GET to /health works (exempted/standard GET)"""
    response = client.get('/health')
    assert response.status_code == 200
