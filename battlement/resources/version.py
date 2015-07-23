import falcon

from battlement.resources import common


class VersionResource(common.APIResource):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = self.format_response_body({
            'API Version': '1',
            'Service Version': '0.0.1'
        })
