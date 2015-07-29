from oslo_log import log

from battlement.queue import handlers
from battlement.plugins import ProvisionerPluginBase

LOG = log.getLogger(__name__)


class SymantecProvisioner(ProvisionerPluginBase):

    def __init__(self, db_manager):
        self._task_handler = SymantecTaskHandler(db_manager)

    def name(self):
        return 'symantec'

    @property
    def task_handler(self):
        return self._task_handler


class SymantecTaskHandler(handlers.CertificateTaskHandler):

    def issue(self, ctx, certificate_uuid, task_uuid):
        LOG.info('Issuing cert with symantec')

    def check(self, ctx, certificate_uuid, task_uuid):
        LOG.info('Checking cert with symantec')

    def update(self, ctx, certificate_uuid, task_uuid):
        raise NotImplementedError

    def revoke(self, ctx, certificate_uuid, task_uuid):
        raise NotImplementedError

    def cancel(self, ctx, certificate_uuid, task_uuid):
        raise NotImplementedError
