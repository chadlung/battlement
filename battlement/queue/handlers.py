import abc

from oslo_log import log
from battlement import queue

LOG = log.getLogger(__name__)


class EchoTaskHandler(queue.MessagingBase):
    def echo(self, ctx, *args, **kwargs):
        LOG.info('echo: {}'.format(kwargs))
        return True


class CertificateTaskHandler(queue.MessagingBase):
    __metaclass__ = abc.ABCMeta

    def __init__(self, db_manager):
        self.db = db_manager

    @abc.abstractmethod
    def issue(self, ctx, certificate_uuid, task_uuid):
        pass

    @abc.abstractmethod
    def check(self, ctx, certificate_uuid, task_uuid):
        pass

    @abc.abstractmethod
    def update(self, ctx, certificate_uuid, task_uuid):
        pass

    @abc.abstractmethod
    def revoke(self, ctx, certificate_uuid, task_uuid):
        pass

    @abc.abstractmethod
    def cancel(self, ctx, certificate_uuid, task_uuid):
        pass
