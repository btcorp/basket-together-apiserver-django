from django.http import HttpResponse, JsonResponse
from django.shortcuts import render_to_response, render, redirect


def index(request):
    return render(request, 'recruit/index.html', {})


def post_list(request):
    data = [
        {'id':1, 'title':'title 1'}
    ]
    return JsonResponse(data, safe=False)
