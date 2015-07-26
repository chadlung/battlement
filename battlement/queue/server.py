from battlement import queue

import oslo_messaging


class MessagingServer(queue.MessagingBase):
    def __init__(self):
        super(MessagingServer, self).__init__(True)

        self.endpoints = [
            EchoTaskHandler()
        ]
        self.server = oslo_messaging.get_rpc_server(
            self.transport,
            self.target,
            self.endpoints,
            executor='eventlet'
        )

    def start(self):
        print('Starting Worker')
        try:
            self.server.start()
            self.server.wait()
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        print('Stopping Worker')
        self.server.stop()


class EchoTaskHandler(queue.MessagingBase):
    def echo(self, ctx):
        print(ctx)
        return True
