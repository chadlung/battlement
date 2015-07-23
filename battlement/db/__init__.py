import os
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy.orm import scoping

db_path = os.path.join(os.path.abspath(os.path.curdir), 'db.sqlite')
db_connection = 'sqlite:///{}'.format(db_path)
db_engine = sqlalchemy.create_engine(db_connection)
DBSession = scoping.scope_session(
    orm.session_maker(bind=db_engine, autocommit=True)
)


def get_session():
    return DBSession()
