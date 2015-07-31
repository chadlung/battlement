import abc

from oslo_log import log
from battlement import queue, utils
from battlement.db.models import task, certificates

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

    def __init__(self, db_manager, cfg=None):
        super(CertificateTaskHandler, self).__init__()
        self.db = db_manager
        self.cfg = cfg

    def _to_check_workflow(self, current_task, msg):
        with self.db.session.begin():
            new_task = task.TaskModel(
                provisioner=current_task.provisioner,
                task_type=task.TaskType.check,
                task_desc=msg or 'Waiting on Changes',
                certificate_id=current_task.certificate_id
            )

            self.db.session.add(new_task)
            current_task.result = 'success'

    def _to_recheck_workflow(self, current_task):
        with self.db.session.begin():
            current_task.active = True
            current_task.recheck_time = utils.recheck_time(120)

    def _to_completed_workflow(self, current_task, cert_model, certificate,
                               intermediates):
        with self.db.session.begin():
            current_task.result = 'success'
            cert_model.certificate = certificate
            cert_model.status = certificates.CertificateStatus.complete

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
