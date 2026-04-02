from app import app
import unittest
from unittest.mock import patch
from bs4 import BeautifulSoup

class TestCSRFProtection(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.manager.search_all')
    def test_search_post_without_csrf_fails(self, mock_search):
        # Attempt to POST to the search route without any CSRF token
        # Now it should fail (return 400 because CSRF protection is enabled)
        response = self.app.post('/', data={
            'location': 'newmarket',
            'price_min': '1000',
            'price_max': '2000'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 400)

    @patch('app.manager.search_all')
    def test_search_post_with_csrf_succeeds(self, mock_search):
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

        with self.app as c:
            # 1. Get the form to establish session and get the token
            response = c.get('/')
            soup = BeautifulSoup(response.data, 'html.parser')
            csrf_token = soup.find('input', {'name': 'csrf_token'})['value']

            # 2. Submit the form with the token
            response = c.post('/', data={
                'csrf_token': csrf_token,
                'location': 'newmarket',
                'price_min': '1000',
                'price_max': '2000'
            }, follow_redirects=True)

            self.assertEqual(response.status_code, 200)

    @patch('app.manager.search_all')
    def test_api_search_without_csrf_succeeds(self, mock_search):
        mock_search.return_value = {
            "listings": [],
            "stats": {},
            "errors": {}
        }

        # API endpoint is exempted, so it should succeed without CSRF
        response = self.app.post('/api/search',
                                json={'location': 'newmarket'},
                                follow_redirects=True)

        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
