from oslo_config import cfg as oslo
from oslo_log import log

from battlement.db.models import task, certificates
from battlement.queue import handlers
from battlement.plugins import ProvisionerPluginBase

LOG = log.getLogger(__name__)


class SymantecProvisioner(ProvisionerPluginBase):
    schema = {
        'type': 'object',
        'properties': {
            'order_id': {'type': 'string'}
        }
    }

    def __init__(self, db_manager):
        super(SymantecProvisioner, self).__init__(db_manager, True)
        self._task_handler = SymantecTaskHandler(db_manager, self.cfg)

    def config_options(self, cfg):
        auth_group = oslo.OptGroup(name='auth')
        auth_options = [
            oslo.StrOpt('partner_code'),
            oslo.StrOpt('username'),
            oslo.StrOpt('password')
        ]

        general_group = oslo.OptGroup(name='general')
        general_options = [
            oslo.StrOpt('endpoint')
        ]

        cfg.register_group(auth_group)
        cfg.register_group(general_group)

        cfg.register_opts(auth_options, group=auth_group)
        cfg.register_opts(general_options, group=general_group)

        return cfg

    @property
    def name(self):
        return 'symantec'

    @property
    def task_handler(self):
        return self._task_handler


class SymantecTaskHandler(handlers.CertificateTaskHandler):
    def __init__(self, db_manager, cfg=None):
        super(SymantecTaskHandler, self).__init__(db_manager, cfg)
        self.credentials = {
            'username': cfg.auth.username,
            'password': cfg.auth.password,
            'partner_code': cfg.auth.partner_code
        }

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
