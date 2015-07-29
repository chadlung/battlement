from battlement import queue
import oslo_messaging


class MessagingClient(queue.MessagingBase):
    def __init__(self):
        super(MessagingClient, self).__init__()
        self.client = oslo_messaging.RPCClient(self.transport, self.target)

    def echo(self, msg=None):
        return self.client.cast({}, 'echo', msg=msg)

    def _cast_cert_msg(self, method, certificate_uuid, task_uuid):
        return self.client.cast(
            {},
            method,
            certificate_uuid=certificate_uuid,
            task_uuid=task_uuid
        )

    def issue(self, certificate_uuid, task_uuid):
        return self._cast_cert_msg('issue', certificate_uuid, task_uuid)

    def check(self, certificate_uuid, task_uuid):
        return self._cast_cert_msg('check', certificate_uuid, task_uuid)

    def update(self, certificate_uuid, task_uuid):
        return self._cast_cert_msg('update', certificate_uuid, task_uuid)

    def revoke(self, certificate_uuid, task_uuid):
        return self._cast_cert_msg('revoke', certificate_uuid, task_uuid)

    def cancel(self, certificate_uuid, task_uuid):
        return self._cast_cert_msg('cancel', certificate_uuid, task_uuid)
