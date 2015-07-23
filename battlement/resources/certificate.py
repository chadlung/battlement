from battlement.resources import common


general_certificate_creation = {
    'type': 'object',
    'required': ['provisoner', 'provision_type', 'provision_data'],
    'properties': {
        'provisoner': {'type': 'string'},
        'provision_type': {'type': 'string'},
        'provision_data': {
            'type': ['string', 'object'],
            'required': ['csr', 'certificate_type', 'approval_email_address'],
            'properties': {
                'csr': {'type': 'string'},
                'certificate_type': {'type': 'string'},
                'approval_email_address': {'type': 'string'}
            }
        }
    }
}


class CertificatesResource(common.APIResource):
    @common.validate(general_certificate_creation)
    def on_post(self, req, resp):
        resp.body = self.format_response_body({
            'certificate_ref': 'https://localhost/v1/certificates/7bd5a553-7258-44bb-b195-457c2bdcff40'
        })
