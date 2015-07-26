from tests.base import AppTestCase


class TestVersionResource(AppTestCase):
    def test_get_version(self):
        resp = self.app.get('/')

        self.assertEqual(resp.status_int, 200)
        self.assertEqual(resp.json.get('API Version'), 'v1')
        self.assertEqual(resp.json.get('Service Version'), '0.0.1')
