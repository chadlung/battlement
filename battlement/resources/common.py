import json
import jsonschema
import falcon


class APIResource(object):
    def format_response_body(self, body_dict):
        return json.dumps(body_dict)

    def abort(self, status=falcon.HTTP_500, message=None):
        """
        Helper function for aborting an API request process. Useful for error
        reporting and exception handling.
        """
        raise falcon.HTTPError(status, message)

    def load_body(self, req, validator=None):
        """
        Helper function for loading an HTTP request body from JSON into a
        Python dictionary
        """
        try:
            raw_json = req.stream.read()
        except Exception:
            self.abort(falcon.HTTP_500, 'Read Error')

        try:
            obj = json.loads(raw_json)
        except ValueError:
            self.abort(falcon.HTTP_400, 'Malformed JSON')

        return obj


def validate(schema):
    def request_decorator(func):
        def wrapper(self, req, resp, *args, **kwargs):
            json_body = self.load_body(req)
            jsonschema.validate(json_body, schema)
            func(self, req, resp, *args, **kwargs)
        return wrapper
    return request_decorator
