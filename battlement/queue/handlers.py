import abc

from oslo_log import log
from battlement import queue

LOG = log.getLogger(__name__)


class EchoTaskHandler(queue.MessagingBase):
    def echo(self, ctx, *args, **kwargs):
        LOG.info('echo: {}'.format(kwargs))
        return True


class CertificatePluginHandler(queue.MessagingBase):
    """ Proxy handler that distributes calls to plugin handlers."""
    def __init__(self, plugin_manager):
        super(CertificatePluginHandler, self).__init__()
        self.plugin_mgr = plugin_manager

    def issue(self, ctx, plugin_name, certificate_uuid, task_uuid):
        plugin = self.plugin_mgr.get_plugin_by_name(plugin_name)
        plugin.task_handler.issue(ctx, certificate_uuid, task_uuid)

    def check(self, ctx, plugin_name, certificate_uuid, task_uuid):
        plugin = self.plugin_mgr.get_plugin_by_name(plugin_name)
        plugin.task_handler.check(ctx, certificate_uuid, task_uuid)

    def update(self, ctx, plugin_name, certificate_uuid, task_uuid):
        plugin = self.plugin_mgr.get_plugin_by_name(plugin_name)
        plugin.task_handler.update(ctx, certificate_uuid, task_uuid)

    def revoke(self, ctx, plugin_name, certificate_uuid, task_uuid):
        plugin = self.plugin_mgr.get_plugin_by_name(plugin_name)
        plugin.task_handler.revoke(ctx, certificate_uuid, task_uuid)

    def cancel(self, ctx, plugin_name, certificate_uuid, task_uuid):
        plugin = self.plugin_mgr.get_plugin_by_name(plugin_name)
        plugin.task_handler.cancel(ctx, certificate_uuid, task_uuid)


class CertificateTaskHandler(queue.MessagingBase):
    __metaclass__ = abc.ABCMeta

    def __init__(self, db_manager):
        super(CertificateTaskHandler, self).__init__()
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
