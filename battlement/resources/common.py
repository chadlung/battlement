import json

class APIResource(object):
    def format_response_body(self, body_dict):
        return json.dumps(body_dict)
