import falcon

from battlement.db.models import project


class NoAuthMiddleware(object):
    def __init__(self, db_manager):
        self.db = db_manager

    def process_request(self, req, resp):
        project_id = req.get_header('X-Project-Id')

        if not project_id:
            desc = 'Please provide your X-Project-Id in the headers.'
            raise falcon.HTTPUnauthorized('Project id required', desc)

        # Create project if not found
        model = project.ProjectModel.get_by_external_id(
            project_id,
            self.db.session
        )
        if not model:
            model = project.ProjectModel(external_id=project_id)
            model.save(self.db.session)

        req.context.update({
            'project': model.id,
            'external_id': project_id
        })
