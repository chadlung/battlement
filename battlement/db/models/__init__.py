import json
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import types as sa_types
from sqlalchemy.ext.declarative import declarative_base

from battlement import utils

SAModel = declarative_base()


class JsonBlob(sa_types.TypeDecorator):
    """JsonBlob is custom type for fields which need to store JSON text."""
    impl = sa.Text

    def process_bind_param(self, value, dialect):
        if value is not None:
            return json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return json.loads(value)
        return value


class ModelBase(object):
    id = sa.Column(sa.String(36), primary_key=True, default=utils.new_uuid)
    created_at = sa.Column(sa.DateTime, default=datetime.utcnow)
    updated_at = sa.Column(
        sa.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def __init__(self, id=None, created_at=None, updated_at=None):
        self.id = id
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def from_dict(cls, json_dict):
        return cls(**json_dict)

    def save(self, session):
        with session.begin():
            session.add(self)
