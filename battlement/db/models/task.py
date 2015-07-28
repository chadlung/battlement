import sqlalchemy as sa
from battlement import utils
from battlement.db import models


class TaskModel(models.ModelBase, models.SAModel):
    __tablename__ = 'tasks'
    active = sa.Column(sa.Boolean, default=False)
    result = sa.Column(sa.String(255), nullable=True)
    errors = sa.Column(models.JsonBlob(), nullable=True)
    next_recheck = sa.Column(sa.DateTime, default=utils.recheck_time)
    task_type = sa.Column(
        sa.String(255),
        default='waiting on ca',
        nullable=False
    )
    certificate_id = sa.Column(
        sa.String(36),
        sa.ForeignKey('certificates.id'),
        index=True,
        nullable=False
    )

    def __init__(self, id=None, certificate_id=None, active=False, result=None,
                 errors=None, next_recheck=None, task_type=None):
        super(TaskModel, self).__init__(id=id)
        self.certificate_id = certificate_id
        self.active = active
        self.result = result
        self.errors = errors
        self.next_recheck = next_recheck
        self.task_type = task_type

    def to_dict(self):
        body_dict = super(TaskModel, self).to_dict()
        body_dict.update({
            'type': self.task_type,
        })

        if self.errors:
            body_dict['errors'] = self.errors.get('msgs', [])
        if self.result:
            body_dict['result'] = self.results
        return body_dict
