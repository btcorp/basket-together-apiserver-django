import json
from django.http import JsonResponse
from django.db.models.query import QuerySet
from django.db.models import Model
from django.shortcuts import get_object_or_404
from recruit.encoder import JSONEncoder


class JSONMiddleware(object):
    def process_response(self, request, response):
        if isinstance(response, (QuerySet, Model)):
            return JsonResponse(response, safe=False, encoder=JSONEncoder,
                                json_dumps_params={'ensure_ascii': False, 'sort_keys': True, 'indent': 4})
        return response
