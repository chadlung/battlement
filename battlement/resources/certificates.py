import falcon

from battlement.db.models import certificates, task
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
    def __init__(self, db_manager, plugin_manager):
        super(CertificatesResource, self).__init__(db_manager)
        self.plugin_manager = plugin_manager

    def _validate_provisioner(self, json_body):
        plugin_name = json_body['provisioner']
        plugin = self.plugin_manager.get_plugin_by_name(plugin_name)
        if not plugin:
            msg = "'{}' is not a supported provisioner".format(plugin_name)
            raise falcon.HTTPBadRequest('Unsupported provisioner', msg)

        plugin.validate_json(json_body)

    @common.load_and_validate(general_certificate_creation)
    def on_post(self, req, resp, json_body):
        self._validate_provisioner(json_body)

        with self.db.session.begin():
            cert_model = certificates.CertificateModel.from_dict(json_body)
            cert_model.project_id = req.context['project']

            initial_task = task.TaskModel(
                certificate_id=cert_model.id,
                task_type=task.TaskType.issue,
                provisioner=cert_model.provisioner
            )
            self.db.session.add(cert_model)
            self.db.session.add(initial_task)

        ref = common.get_full_url('/v1/certificates/{}'.format(cert_model.id))
        resp.body = self.format_response_body({'certificate_ref': ref})


class CertificateResource(common.APIResource):
    def on_get(self, req, resp, uuid):
        model = certificates.CertificateModel.get(
            uuid,
            req.context['project'],
            self.db.session
        )

        if not model:
            resp.status = falcon.HTTP_404
            return

        model.tasks = model.load_tasks(self.db.session)

        body_dict = model.to_dict()
        resp.body = self.format_response_body(body_dict)

    def on_delete(self, req, resp, uuid):
        project_id = req.context['project']
        model = certificates.CertificateModel.get(
            uuid,
            project_id,
            self.db.session
        )
        if model:
            model.delete(project_id, self.db.session)
            resp.status = falcon.HTTP_204
        else:
            resp.status = falcon.HTTP_404
