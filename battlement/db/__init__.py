import os
import urlparse
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy.orm import scoping

from battlement.config import cfg
from battlement.db import models

db_connection = cfg.get('db', 'connection')
db_engine = sqlalchemy.create_engine(db_connection)

DBSession = scoping.scoped_session(
    orm.sessionmaker(bind=db_engine, autocommit=True)
)


def get_session():
    return DBSession()


def setup_database():
    parsed_url = urlparse.urlparse(db_connection)
    if parsed_url.scheme == 'sqlite':
        models.SAModel.metadata.create_all(db_engine)
