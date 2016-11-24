import json
from django.http import JsonResponse
from django.db.models.query import QuerySet
from django.db.models import Model
from recruit.encoder import JSONEncoder
from basket_together.json_data_format import *


class JSONMiddleware(object):
    def process_response(self, request, response):
        if isinstance(response, (QuerySet, Model, dict)):
            data = JsonResponse(response, safe=False, encoder=JSONEncoder)
            return output_format_json_response(200, statusCode='0000', data=json.loads(data.content))
        return response
