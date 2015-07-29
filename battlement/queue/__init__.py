import oslo_messaging
from battlement.config import cfg


def create_target(exchange=None, topic=None, namespace=None,
                  server=None, version=None):
    target = oslo_messaging.Target(
        topic=topic or cfg.queue.topic,
        namespace=namespace or cfg.queue.namespace,
        version=version or cfg.queue.version,
        server=server,
        exchange=exchange
    )
    return target


class MessagingBase(object):

    def __init__(self, is_server=False, exchange=None):
        server_name = cfg.queue.server_name if is_server else None
        self.transport = oslo_messaging.get_transport(cfg)
        self.target = create_target(server=server_name, exchange=exchange)
