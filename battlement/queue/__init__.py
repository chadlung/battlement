import oslo_messaging
from battlement.config import cfg


class MessagingBase(object):
    def __init__(self, is_server=False):
        server = cfg.queue.server_name if is_server else None
        self.transport = oslo_messaging.get_transport(cfg)
        self.target = oslo_messaging.Target(
            topic=cfg.queue.topic,
            namespace=cfg.queue.namespace,
            server=server,
            version=cfg.queue.version
        )
