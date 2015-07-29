from oslo_log import log

from battlement.db.models import task, certificates
from battlement.queue import handlers
from battlement.plugins import ProvisionerPluginBase

LOG = log.getLogger(__name__)


class SymantecProvisioner(ProvisionerPluginBase):

    def __init__(self, db_manager):
        super(SymantecProvisioner, self).__init__(db_manager)
        self._task_handler = SymantecTaskHandler(db_manager)

    @property
    def name(self):
        return 'symantec'

    @property
    def task_handler(self):
        return self._task_handler

    def validate_json(self, json_dict):
        pass


class SymantecTaskHandler(handlers.CertificateTaskHandler):
    def issue(self, ctx, certificate_uuid, task_uuid):
        current_task = task.TaskModel.get(task_uuid, None, self.db.session)

        # TODO(jmvrbanac): Implement cert issue to Symantec

        self._to_check_workflow(current_task, 'Waiting on CA')
        LOG.info('Issued cert with Symantec - WIP')

    def check(self, ctx, certificate_uuid, task_uuid):
        current_task = task.TaskModel.get(task_uuid, None, self.db.session)
        cert = certificates.CertificateModel.get(
            certificate_uuid,
            project_id=None,
            session=self.db.session
        )

        # TODO(jmvrbanac): Implement cert check to Symantec

        # Assuming it was found
        self._to_completed_workflow(current_task, cert)

        LOG.info('Checked cert with Symantec - WIP')

    def update(self, ctx, certificate_uuid, task_uuid):
        raise NotImplementedError

    def revoke(self, ctx, certificate_uuid, task_uuid):
        raise NotImplementedError

    def cancel(self, ctx, certificate_uuid, task_uuid):
        raise NotImplementedError
