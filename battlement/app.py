import falcon

from battlement import db
from battlement.resources.version import VersionResource
from battlement.resources.provisioner import ProvisionersResource
from battlement.resources.certificate import CertificatesResource


class BattlementApp(falcon.API):
    def __init__(self):
        super(BattlementApp, self).__init__()
        db.setup_database()

        self.add_route('/', VersionResource())
        self.add_route('/v1/provisioners', ProvisionersResource())
        self.add_route('/v1/certificates', CertificatesResource())


application = BattlementApp()
