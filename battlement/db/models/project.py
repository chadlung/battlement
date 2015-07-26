import sqlalchemy as sa

from battlement.db import models


class ProjectModel(models.ModelBase, models.SAModel):
    __tablename__ = 'projects'
    external_id = sa.Column(sa.String(255), unique=True)

    def __init__(self, id=None, external_id=None):
        super(ProjectModel, self).__init__(id)
        self.external_id = external_id

    @classmethod
    def get_by_external_id(cls, external_id, session):
        model = None
        with session.begin():
            query = session.query(ProjectModel)
            query = query.filter_by(external_id=external_id)
            model = query.first()

        return model
