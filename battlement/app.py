import falcon

from battlement.resources.version import VersionResource


class BattlementApp(falcon.API):
    def __init__(self):
        super(BattlementApp, self).__init__()
        self.add_route('/', VersionResource())


application = BattlementApp()
