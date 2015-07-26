from tests.base import AppTestCase

create_data = {
    'provisioner': 'symantec',
    'provision_type': 'csr',
    'provision_data': {
        'csr': 'boo',
        'certificate_type': 'foo',
        'approval_email_address': 'floo'
    }
}


class TestCertificatesResource(AppTestCase):
    def test_create_certificate(self):
        resp = self.app.post_json('/v1/certificates', create_data)
        self.assertEqual(resp.status_int, 200)

        cert_ref = resp.json.get('certificate_ref')
        self.assertIn('/v1/certificates/', cert_ref)


class TestCertificateResource(AppTestCase):
    def test_retrieve(self):
        resp = self.app.post_json('/v1/certificates', create_data)
        self.assertEqual(resp.status_int, 200)

        cert_ref = self.app_ref(resp.json.get('certificate_ref'))
        resp = self.app.get(cert_ref)

        self.assertEqual(resp.status_int, 200)
        self.assertEqual(resp.json.get('provisioner'), 'symantec')
        self.assertEqual(resp.json.get('provision_type'), 'csr')
        self.assertIsNotNone(resp.json.get('provision_data'))

    def test_delete(self):
        resp = self.app.post_json('/v1/certificates', create_data)
        self.assertEqual(resp.status_int, 200)

        cert_ref = self.app_ref(resp.json.get('certificate_ref'))

        resp = self.app.delete(cert_ref)
        self.assertEqual(resp.status_int, 204)
