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
    created = sa.Column(sa.DateTime, default=datetime.utcnow)
    updated = sa.Column(
        sa.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def __init__(self, id=None, created=None, updated=None):
        self.id = id or utils.new_uuid()
        self.created = created
        self.updated = updated

    @classmethod
    def _query_by_uuid(cls, uuid, project_id, session):
        query = session.query(cls)
        query = query.filter_by(id=uuid)
        if project_id:
            query = query.filter_by(project_id=project_id)
        return query

    @classmethod
    def from_dict(cls, json_dict):
        return cls(**json_dict)

    def to_dict(self):
        return {
            'id': self.id,
            'created': self.created.isoformat(),
            'updated': self.updated.isoformat()
        }

    def save(self, session):
        with session.begin():
            session.add(self)

    def delete(self, project_id, session):
        result = False
        with session.begin():
            query = self._query_by_uuid(self.id, project_id, session)
            result = query.delete() == 1
        return result

    @classmethod
    def get(cls, uuid, project_id, session):
        model = None
        with session.begin():
            query = cls._query_by_uuid(uuid, project_id, session)
            model = query.first()
        return model

    @classmethod
    def get_page(cls, project_id, offset, limit, session):
        models = []
        with session.begin():
            query = session.query(cls)
            query = query.filter_by(project_id=project_id)
            query = query.offset(offset)
            query = query.limit(limit)
            models = query.all()
        return models

    @classmethod
    def project_total(cls, project_id, session):
        total = 0
        with session.begin():
            query = session.query(cls.id)
            query = query.filter_by(project_id=project_id)
            total = query.count()
        return total
