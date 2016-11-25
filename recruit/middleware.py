import json

from django.db.models import Model
from django.db.models.query import QuerySet

from basket_together.json_data_format import *
from recruit.encoder import JSONEncoder


class JSONMiddleware(object):
    def process_response(self, request, response):
        if isinstance(response, (QuerySet, Model, dict)):
            data = json.dumps(response, cls=JSONEncoder)
            return output_format_json_response(200, statusCode='0000', data=json.loads(data))
        return response
