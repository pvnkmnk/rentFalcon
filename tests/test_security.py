from app import app
import pytest

def test_csrf_active():
    # Now that CSRF is enabled, this POST request without a token should fail (400)
    with app.test_client() as client:
        response = client.post('/', data={'location': 'newmarket'})
        print(f"Response status: {response.status_code}")
        # Flask-WTF returns 400 for missing CSRF token by default
        assert response.status_code == 400

def test_api_csrf_exempt():
    # API endpoint should still work without CSRF token because it is exempt
    with app.test_client() as client:
        # Mocking the manager.search_all to avoid actual scraping in this test
        # but for now let's just see if it gets past CSRF.
        # Since I'm using the real app, it might try to scrape.
        # Let's just check if it's NOT a 400/403.
        response = client.post('/api/search', json={'location': 'newmarket'})
        print(f"API Response status: {response.status_code}")
        assert response.status_code != 400
        assert response.status_code != 403

if __name__ == "__main__":
    try:
        test_csrf_active()
        print("test_csrf_active passed")
        test_api_csrf_exempt()
        print("test_api_csrf_exempt passed")
    except AssertionError as e:
        print(f"Test failed: {e}")
        exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)
