import unittest
import json
from unittest.mock import patch
from app import app

class TestSecurity(unittest.TestCase):
    def setUp(self):
        # Configure app for testing with CSRF enabled
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = True
        app.config['SECRET_KEY'] = 'test-secret-key'
        self.client = app.test_client()

    def test_post_form_without_csrf_fails(self):
        """
        Verify that POST requests to the main form WITHOUT a CSRF token now fail.
        """
        # Ensure we're hitting the '/' route with POST data
        response = self.client.post('/', data={
            'location': 'Newmarket',
            'price_min': '1000',
            'price_max': '2000'
        })
        # CSRF failure typically returns 400 (Bad Request)
        self.assertEqual(response.status_code, 400)

    def test_post_api_without_csrf_succeeds(self):
        """
        Verify that POST requests to the API endpoint succeed WITHOUT a CSRF token
        due to the exemption.
        """
        # We need to mock the scraper manager to avoid actual scraping during tests
        with patch('app.manager.search_all') as mocked_search:
            mocked_search.return_value = {
                'listings': [],
                'stats': {'scrapers_succeeded': 0, 'execution_time': 0, 'scrapers_failed': 0},
                'errors': {}
            }
            response = self.client.post('/api/search',
                                     data=json.dumps({'location': 'Newmarket'}),
                                     content_type='application/json')
            self.assertEqual(response.status_code, 200)

    def test_csrf_token_present_in_form(self):
        """
        Verify that the CSRF token is actually rendered in the HTML form.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'name="csrf_token"', response.data)

if __name__ == '__main__':
    unittest.main()
