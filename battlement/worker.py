import eventlet
eventlet.monkey_patch()

from battlement.queue.server import MessagingServer


def main():
    worker = MessagingServer()
    worker.start()

if __name__ == '__main__':
    main()
