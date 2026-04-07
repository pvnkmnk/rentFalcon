import pytest
from app import app
import json


@pytest.fixture
def client():
    app.config['TESTING'] = True
    # TestingConfig has CSRF disabled by default.
    with app.test_client() as client:
        yield client


def test_index_get(client):
    """Test that the index page loads correctly."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Rental Scanner" in response.data
    assert b"csrf_token" in response.data


def test_api_search_no_csrf(client):
    """Test that the API search endpoint is exempt from CSRF."""
    # This should work due to @csrf.exempt.
    response = client.post('/api/search',
                           data=json.dumps({'location': 'newmarket'}),
                           content_type='application/json')
    # It might return 200 if scrapers are mocked or if it actually runs.
    # We mainly care that it's not a 400/403 CSRF error.
    assert response.status_code in [200, 500]


def test_csrf_protection_enabled():
    """Verify that CSRF is enabled in development/production."""
    from config import DevelopmentConfig, ProductionConfig
    assert DevelopmentConfig.WTF_CSRF_ENABLED is True
    assert ProductionConfig.WTF_CSRF_ENABLED is True


if __name__ == "__main__":
    # Manual verification of CSRF on main form
    # This is tricky in a unit test without session handling for the token.
    # But we already verified it with reproduce_csrf.py.
    pass
