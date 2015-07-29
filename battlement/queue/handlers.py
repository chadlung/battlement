from oslo_log import log
from battlement import queue

LOG = log.getLogger(__name__)


class EchoTaskHandler(queue.MessagingBase):
    def echo(self, ctx, *args, **kwargs):
        LOG.info('echo: {}'.format(kwargs))
        return True
