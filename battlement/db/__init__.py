import os
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy.orm import scoping

from battlement.db import models

db_path = os.path.join(os.path.abspath(os.path.curdir), 'db.sqlite')
db_connection = 'sqlite:///{}'.format(db_path)
db_engine = sqlalchemy.create_engine(db_connection)
DBSession = scoping.scoped_session(
    orm.sessionmaker(bind=db_engine, autocommit=True)
)


def get_session():
    return DBSession()


def setup_database():
    if not os.path.exists(db_path):
        print('Could not find db on path, creating a new one')
        models.SAModel.metadata.create_all(db_engine)
