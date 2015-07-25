import sqlalchemy as sa

from battlement.db import models


class CertificateModel(models.ModelBase, models.SAModel):
    __tablename__ = 'certificates'
    provisioner = sa.Column(sa.String(255), nullable=False)
    provision_type = sa.Column(sa.String(255), nullable=False)
    provision_data = sa.Column(models.JsonBlob(), nullable=False)

    def __init__(self, id=None, created_at=None, updated_at=None,
                 provisioner=None, provision_type=None, provision_data=None):
        super(CertificateModel, self).__init__(id, created_at, updated_at)
        self.provisioner = provisioner
        self.provision_type = provision_type
        self.provision_data = provision_data

    def to_dict(self):
        body_dict = super(CertificateModel, self).to_dict()
        body_dict.update({
            'provisioner': self.provisioner,
            'provision_type': self.provision_type,
            'provision_data': self.provision_data
        })
        return body_dict
