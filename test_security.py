import unittest
from app import app


class TestSecurity(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = True
        self.client = app.test_client()

    def test_csrf_on_index_post(self):
        # POST without CSRF token should fail with 400
        response = self.client.post("/", data={"location": "ottawa"})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"The CSRF token is missing", response.data)

    def test_api_search_csrf_exempt(self):
        # API search should be exempt and return 400 (Bad Request) if missing location,
        # but NOT 400 (CSRF error)
        response = self.client.post("/api/search", json={})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data["error"], "Location is required")


if __name__ == "__main__":
    unittest.main()
