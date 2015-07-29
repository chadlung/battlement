import eventlet
eventlet.monkey_patch()

from oslo_log import log
from battlement import config, db, plugins
from battlement.queue.server import MessagingServer


def main():
    log.setup(config.cfg, 'battlement')

    db_manager = db.DBManager()
    db_manager.setup()

    plugin_mgr = plugins.PluginManager(db_manager)
    worker = MessagingServer(db_manager, plugin_mgr)
    worker.start()


if __name__ == '__main__':
    main()
