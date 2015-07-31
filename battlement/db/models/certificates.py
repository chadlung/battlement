from enum import IntEnum
import sqlalchemy as sa

from battlement.db import models
from battlement.db.models import task, project


class CertificateStatus(IntEnum):
    in_progress = 1
    complete = 2


class CertificateModel(models.ModelBase, models.SAModel):
    __tablename__ = 'certificates'
    provisioner = sa.Column(sa.String(255), nullable=False)
    provision_type = sa.Column(sa.String(255), nullable=False)
    provision_data = sa.Column(models.JsonBlob(), nullable=False)
    plugin_data = sa.Column(models.JsonBlob(), nullable=True)
    certificate = sa.Column(sa.Text(), nullable=True)
    status = sa.Column(
        sa.SmallInteger(),
        default=CertificateStatus.in_progress,
        nullable=False
    )
    project_id = sa.Column(
        sa.String(36),
        sa.ForeignKey(project.ProjectModel.id),
        index=True,
        nullable=False
    )

    def __init__(self, id=None, external_id=None, created=None, updated=None,
                 provisioner=None, provision_type=None, provision_data=None,
                 certificate=None, *arg, **kwargs):
        super(CertificateModel, self).__init__(id, created, updated)
        self.project_id = external_id
        self.provisioner = provisioner
        self.provision_type = provision_type
        self.provision_data = provision_data
        self.certificate = certificate
        self.tasks = []
        self.plugin_data = kwargs.get(provisioner)

    def to_dict(self):
        body_dict = super(CertificateModel, self).to_dict()
        body_dict.update({
            'provisioner': self.provisioner,
            'provision_type': self.provision_type,
            'provision_data': self.provision_data,
            'tasks': [t.to_dict() for t in self.tasks],
            'status': CertificateStatus(self.status).name,
            'certificate': self.certificate,
            self.provisioner: self.plugin_data
        })
        return body_dict

    def to_minimal_dict(self):
        body_dict = super(CertificateModel, self).to_dict()
        body_dict.update({
            'provisioner': self.provisioner,
            'status': CertificateStatus(self.status).name,
        })
        return body_dict

    def load_tasks(self, session):
        tasks = []
        with session.begin():
            query = session.query(task.TaskModel)
            query = query.filter_by(certificate_id=self.id)
            query = query.order_by(sa.desc(task.TaskModel.created))
            tasks = query.all()
        return tasks
