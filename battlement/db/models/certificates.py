import uuid
from datetime import datetime

import sqlalchemy as sa

from battlement.db import models


class CertificateModel(models.ModelBase):
    __tablename__ = 'certificates'
    id = sa.Column(sa.String(36), primary_key=True, default=uuid.uuid4)
    provisioner = sa.Column(sa.String(255), nullable=False)
    provision_type = sa.Column(sa.String(255), nullable=False)
    provision_data = sa.Column(sa.Text, nullable=False)
    created_at = sa.Column(sa.DateTime, default=datetime.utcnow)
    updated_at = sa.Column(
        sa.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

