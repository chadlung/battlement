from tests.base import AppTestCase


class TestProvisionerResource(AppTestCase):
    def test_get_provisioners(self):
        resp = self.get('/v1/provisioners')

        self.assertEqual(resp.status_int, 200)

        provisioners = resp.json.get('provisioners')
        self.assertEqual(len(provisioners), 2)
        self.assertIn('symantec', provisioners)
        self.assertIn('dogtag', provisioners)
