
from battlement import queue
from battlement.db.models import task, certificates  # noqa
from battlement.queue import client, handlers

from oslo_log import log
import oslo_messaging
from oslo_service import service

LOG = log.getLogger(__name__)


class MessagingServer(queue.MessagingBase):
    def __init__(self, exchange=None):
        super(MessagingServer, self).__init__(True, exchange)

        self.server = oslo_messaging.get_rpc_server(
            self.transport,
            self.target,
            self.endpoints,
            executor='eventlet'
        )

    @property
    def endpoints(self):
        return [handlers.EchoTaskHandler()]

    def start(self):
        try:
            self.server.start()
            LOG.info('Started Worker')
            self.server.wait()
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        self.server.stop()
        LOG.info('Stopped Worker')


class QueuingServer(service.Service):
    def __init__(self, db_manager, startup_delay=5, recheck_interval=5):
        super(QueuingServer, self).__init__()
        self.db = db_manager
        self.startup_delay = startup_delay
        self.recheck_interval = recheck_interval

        self.client = client.MessagingClient()

        self.tg.add_dynamic_timer(
            self.check_tasks,
            initial_delay=self.startup_delay,
            periodic_interval_max=self.recheck_interval
        )

    def check_tasks(self):
        LOG.info('Checking for updates...')
        tasks = task.get_tasks_to_queue(self.db.session)
        LOG.info('Found {} task(s) to process'.format(len(tasks)))
        for work_task in tasks:
            with self.db.session.begin():
                work_task.active = True
                task_id = work_task.id

                LOG.info('Queuing task: {id}'.format(id=task_id))
                self.client.echo('I got task {}'.format(task_id))

        return self.recheck_interval

    def start(self):
        try:
            super(QueuingServer, self).start()
            LOG.info('Started Queue Manager')
            self.wait()
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        super(QueuingServer, self).stop()
        LOG.info('Stopped Queue Manager')
