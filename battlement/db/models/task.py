from datetime import datetime
from enum import IntEnum

import sqlalchemy as sa
from battlement import utils
from battlement.db import models


class TaskType(IntEnum):
    issue = 1
    check = 2
    update = 3
    revoke = 4
    cancel = 5


class TaskModel(models.ModelBase, models.SAModel):
    __tablename__ = 'tasks'
    active = sa.Column(sa.Boolean, default=False)
    result = sa.Column(sa.String(255), nullable=True)
    errors = sa.Column(models.JsonBlob(), nullable=True)
    provisioner = sa.Column(sa.String(255), nullable=False)
    next_recheck = sa.Column(sa.DateTime, default=utils.recheck_time)
    task_type = sa.Column(
        sa.SmallInteger,
        default=TaskType.check,
        nullable=False
    )
    task_desc = sa.Column(
        sa.String(255),
        nullable=True
    )
    certificate_id = sa.Column(
        sa.String(36),
        sa.ForeignKey('certificates.id'),
        index=True,
        nullable=False
    )

    def __init__(self, id=None, certificate_id=None, active=False, result=None,
                 errors=None, provisioner=None, next_recheck=None,
                 task_type=None, task_desc=None):
        super(TaskModel, self).__init__(id=id)
        self.certificate_id = certificate_id
        self.active = active
        self.result = result
        self.errors = errors
        self.provisioner = provisioner
        self.next_recheck = next_recheck
        self.task_type = task_type
        self.task_desc = task_desc

    def to_dict(self):
        body_dict = super(TaskModel, self).to_dict()
        body_dict.update({
            'type': self.task_type,
        })

        if self.errors:
            body_dict['errors'] = self.errors.get('msgs', [])
        if self.result:
            body_dict['result'] = self.result
        return body_dict


def get_tasks_to_queue(session):
    tasks = []
    with session.begin():
        query = session.query(TaskModel)
        query = query.filter_by(active=False, result=None)
        query = query.filter(TaskModel.next_recheck <= datetime.utcnow())
        tasks = query.all()
    return tasks
