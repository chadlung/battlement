from battlement import queue
import oslo_messaging


class MessagingClient(queue.MessagingBase):
    def __init__(self):
        super(MessagingClient, self).__init__()
        self.client = oslo_messaging.RPCClient(self.transport, self.target)

    def echo(self):
        return self.client.cast({}, 'echo')
