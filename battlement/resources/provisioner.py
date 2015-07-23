import falcon

from battlement import plugins
from battlement.resources.common import APIResource


class ProvisionersResource(APIResource):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = self.format_response_body({
            'provisioners': plugins.get_active_plugin_names()
        })
