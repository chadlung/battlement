import falcon

from oslo_log import log

from battlement import db, config
from battlement.middleware import auth
from battlement.resources.version import VersionResource
from battlement.resources.provisioner import ProvisionersResource
from battlement.resources.certificates import CertificateResource
from battlement.resources.certificates import CertificatesResource


class BattlementApp(falcon.API):
    def __init__(self, db_manager=None):
        log.setup(config.cfg, 'battlement')
        if not db_manager:
            db_manager = db.DBManager()
            db_manager.setup()

        super(BattlementApp, self).__init__(
            middleware=[auth.NoAuthMiddleware(db_manager)]
        )

        version = VersionResource()
        provisioners = ProvisionersResource()
        certificate = CertificateResource(db_manager)
        certificates = CertificatesResource(db_manager)

        self.add_route('/', version)
        self.add_route('/v1/provisioners', provisioners)
        self.add_route('/v1/certificates', certificates)
        self.add_route('/v1/certificates/{uuid}', certificate)

        LOG = log.getLogger(__name__)
        LOG.info('Battlement API Started')


application = BattlementApp()
