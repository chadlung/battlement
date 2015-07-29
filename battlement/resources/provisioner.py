import falcon

from battlement.resources.common import APIResource


class ProvisionersResource(APIResource):
    def __init__(self, plugin_manager):
        super(ProvisionersResource, self).__init__()
        self.plugin_manager = plugin_manager

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = self.format_response_body({
            'provisioners': self.plugin_manager.active_plugin_names
        })
