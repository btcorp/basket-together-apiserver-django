from django.http import JsonResponse


def output_message_json(status=None, **kwargs):
    return JsonResponse(
        {
            'statusCode': kwargs.get('statusCode', ''),
            'errorMessage': kwargs.get('message', ''),
            'data': kwargs.get('data', ''),
        },
        json_dumps_params={'ensure_ascii': False},
        safe=False,
        status=status
    )