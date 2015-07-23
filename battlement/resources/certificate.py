import falcon

from battlement.resources.common import APIResource


class CertificatesResource(APIResource):
    def on_post(self, req, resp):
        body_dict = self.load_body(req)
        #json schema validation here
        resp.body = self.format_response_body({
            'certificate_ref': 'https://localhost/v1/certificates/7bd5a553-7258-44bb-b195-457c2bdcff40'
        })
        
