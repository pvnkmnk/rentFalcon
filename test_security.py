import pytest
from unittest.mock import MagicMock, patch
from app import app
from flask_wtf.csrf import generate_csrf

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = True
    app.config['SECRET_KEY'] = 'test-secret'
    with app.test_client() as client:
        yield client

@patch('app.manager')
def test_index_post_without_csrf_fails(mock_manager, client):
    """
    Verify that POST requests without a CSRF token now fail with 400.
    """
    response = client.post('/', data={'location': 'Newmarket'})
    assert response.status_code == 400

@patch('app.manager')
def test_index_post_with_csrf_succeeds(mock_manager, client):
    """
    Verify that POST requests with a valid CSRF token succeed.
    """
    mock_manager.search_all.return_value = {
        "listings": [],
        "stats": {
            "unique_listings": 0,
            "scrapers_succeeded": 0,
            "duplicates_removed": 0,
            "execution_time": 0.1,
            "by_source": {}
        },
        "errors": {}
    }

    # We need to get a CSRF token first. In a test client, we can do this by
    # visiting the page first.
    client.get('/')
    with client.session_transaction() as session:
        # Flask-WTF stores the CSRF token in the session under '_csrf_token'
        # But we use generate_csrf to get the token for the form.
        pass

    # Simpler way for testing with Flask-WTF:
    # Use a mock or just check if it fails without and passes when disabled.
    # But let's try to do it properly.

    # Since we use app.test_client(), CSRF protection is active.
    # To test with CSRF, we can either:
    # 1. Disable it for this specific test (not ideal for verifying the fix)
    # 2. Extract it from the GET response and include it.

    res = client.get('/')
    # Extract csrf_token from the form in the response
    import re
    match = re.search(r'name="csrf_token" value="([^"]+)"', res.data.decode())
    assert match is not None
    csrf_token = match.group(1)

    response = client.post('/', data={'location': 'Newmarket', 'csrf_token': csrf_token})
    assert response.status_code == 200

def test_api_search_without_csrf_still_succeeds(client):
    """
    Verify that the API endpoint remains accessible without CSRF.
    """
    with patch('app.manager.search_all') as mock_search:
        mock_search.return_value = {"listings": [], "stats": {}, "errors": {}, "timestamp": "...", "search_params": {}}
        response = client.post('/api/search', json={'location': 'Newmarket'})
        assert response.status_code == 200
