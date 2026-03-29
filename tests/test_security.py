import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = True  # Enable CSRF for testing
    app.config['SECRET_KEY'] = 'test-secret-key'
    with app.test_client() as client:
        yield client

def test_index_get(client):
    response = client.get('/')
    assert response.status_code == 200

def test_index_post_no_csrf(client):
    # This should fail (400) because we don't provide a CSRF token
    response = client.post('/', data={'location': 'ottawa'})
    assert response.status_code == 400

def test_api_search_post_exempt(client):
    # This should succeed (200) because it's exempted from CSRF
    response = client.post('/api/search', json={'location': 'ottawa'})
    assert response.status_code == 200
