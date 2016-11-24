from django.http import JsonResponse
from rest_framework.response import Response


def output_format_json_response(status=None, **kwargs):
    return JsonResponse(
        {
            'statusCode': kwargs.get('statusCode', ''),
            'errorMessage': kwargs.get('message', ''),
            'data': kwargs.get('data', ''),
        },
        json_dumps_params={'ensure_ascii': False, 'sort_keys': True, 'indent': 4},
        safe=False,
        status=status
    )


def output_format_response(status=None, **kwargs):
    return Response(
        {
            'statusCode': kwargs.get('statusCode', ''),
            'errorMessage': kwargs.get('message', ''),
            'data': kwargs.get('data', ''),
        },
        status=status
    )