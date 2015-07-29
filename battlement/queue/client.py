from battlement import queue
import oslo_messaging


class MessagingClient(queue.MessagingBase):
    def __init__(self):
        super(MessagingClient, self).__init__()
        self.client = oslo_messaging.RPCClient(self.transport, self.target)

    def echo(self, msg=None):
        return self.client.cast({}, 'echo', msg=msg)

    def _cast_msg(self, method, plugin_name, certificate_uuid, task_uuid):
        return self.client.cast(
            {},
            method,
            plugin_name=plugin_name,
            certificate_uuid=certificate_uuid,
            task_uuid=task_uuid
        )

    def issue(self, plugin_name, certificate_uuid, task_uuid):
        return self._cast_msg(
            'issue',
            plugin_name,
            certificate_uuid,
            task_uuid
        )

    def check(self, plugin_name, certificate_uuid, task_uuid):
        return self._cast_msg(
            'check',
            plugin_name,
            certificate_uuid,
            task_uuid
        )

    def update(self, plugin_name, certificate_uuid, task_uuid):
        return self._cast_msg(
            'update',
            plugin_name,
            certificate_uuid,
            task_uuid
        )

    def revoke(self, plugin_name, certificate_uuid, task_uuid):
        return self._cast_msg(
            'revoke',
            plugin_name,
            certificate_uuid,
            task_uuid
        )

    def cancel(self, plugin_name, certificate_uuid, task_uuid):
        return self._cast_msg(
            'cancel',
            plugin_name,
            certificate_uuid,
            task_uuid
        )
