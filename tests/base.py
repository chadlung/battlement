import unittest
import webtest

from battlement import db, app, config
from battlement.db import models


class DBTestCase(unittest.TestCase):
    def setUp(self):
        super(DBTestCase, self).setUp()
        self._db_manager = db.DBManager('sqlite://')
        self._db_manager.setup()

    def tearDown(self):
        models.SAModel.metadata.drop_all(self._db_manager.engine)
        super(DBTestCase, self).tearDown()


class AppTestCase(DBTestCase):
    def setUp(self):
        super(AppTestCase, self).setUp()
        real_app = app.BattlementApp(self._db_manager)
        self.app = webtest.TestApp(real_app)

    def app_ref(self, full_ref):
        base_ref = config.cfg.get('api', 'base_ref')
        return full_ref.replace(base_ref, '')
