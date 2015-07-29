import eventlet
eventlet.monkey_patch()

from oslo_log import log
from battlement import config
from battlement.queue.server import MessagingServer


def main():
    log.setup(config.cfg, 'battlement')
    worker = MessagingServer()
    worker.start()


if __name__ == '__main__':
    main()
