from battlement import db
from battlement.db.models import certificates
from battlement.resources import common


general_certificate_creation = {
    'type': 'object',
    'required': ['provisioner', 'provision_type', 'provision_data'],
    'properties': {
        'provisioner': {'type': 'string'},
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
    def on_post(self, req, resp, json_body):
        model = certificates.CertificateModel.from_dict(json_body)
        model.save(db.get_session())

        resp.body = self.format_response_body({
            'certificate_ref': 'https://localhost/v1/certificates/{uuid}'
        })
