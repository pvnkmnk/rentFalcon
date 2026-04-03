import pytest
from app import app
from flask import url_for

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = True
    app.config['SECRET_KEY'] = 'test-key'
    with app.test_client() as client:
        yield client

def test_index_get_works(client):
    """Test that GET request to index works"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Search Rentals' in response.data

def test_search_without_csrf_fails(client):
    """Test that POST request without CSRF token fails (400 Bad Request)"""
    response = client.post('/', data={'location': 'newmarket'})
    assert response.status_code == 400
    assert b'The CSRF token is missing' in response.data or b'Bad Request' in response.data

def test_api_search_without_csrf_succeeds(client):
    """Test that API endpoint is exempt from CSRF and succeeds"""
    # Note: We mock the manager to avoid actual scraping during tests
    from unittest.mock import patch
    with patch('app.manager.search_all') as mock_search:
        mock_search.return_value = {
            'listings': [],
            'stats': {'unique_listings': 0, 'scrapers_succeeded': 0, 'duplicates_removed': 0, 'execution_time': 0, 'by_source': {}},
            'errors': {}
        }
        response = client.post('/api/search', json={'location': 'newmarket'})
        assert response.status_code == 200
        assert b'listings' in response.data

def test_search_with_csrf_succeeds(client):
    """Test that POST request with valid CSRF token succeeds"""
    from unittest.mock import patch

    # First get the page to get a CSRF token in the session
    response = client.get('/')
    assert response.status_code == 200

    # Extract CSRF token from the page
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(response.data, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrf_token'})['value']

    with patch('app.manager.search_all') as mock_search:
        mock_search.return_value = {
            'listings': [],
            'stats': {'unique_listings': 0, 'scrapers_succeeded': 0, 'duplicates_removed': 0, 'execution_time': 0, 'by_source': {}},
            'errors': {}
        }
        response = client.post('/', data={
            'location': 'newmarket',
            'csrf_token': csrf_token
        })
        assert response.status_code == 200
        assert b'Listings Found' in response.data or b'No listings found' in response.data
