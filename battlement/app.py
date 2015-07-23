import falcon

from battlement.resources.version import VersionResource
from battlement.resources.provisioner import ProvisionersResource


class BattlementApp(falcon.API):
    def __init__(self):
        super(BattlementApp, self).__init__()
        self.add_route('/', VersionResource())
        self.add_route('/v1/provisioners', ProvisionersResource())


application = BattlementApp()
