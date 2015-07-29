import eventlet
eventlet.monkey_patch()

from oslo_log import log

from battlement import db, config
from battlement.queue.server import QueuingServer


def main():
    log.setup(config.cfg, 'battlement')
    db_manager = db.DBManager()
    db_manager.setup()

    queuing = QueuingServer(db_manager)
    queuing.start()

if __name__ == '__main__':
    main()
