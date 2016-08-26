import ast
from accounts.forms import UserProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.forms import model_to_dict
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from rest_framework.authtoken import views as rest_views
from rest_framework.decorators import api_view


@csrf_exempt
def signup(request):
    byte_to_str = (request.body).decode('utf-8')
    data = ast.literal_eval(byte_to_str)
    form = UserCreationForm(data)
    if form.is_valid():
        user = form.save()
        user_dict = model_to_dict(user, fields=['id', 'username'])
        return JsonResponse(user_dict)
    return JsonResponse(form.errors)


@csrf_exempt
def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.auth_token is not None:
            user.auth_token.delete()
        login(request, user)
        return rest_views.ObtainAuthToken.as_view()(request)    # create token
    else:
        JsonResponse({'error': '에러입니다.'})


@csrf_exempt
@login_required
def user_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('loggedin.html')
    else:
        form = UserProfileForm(instance=request.user.profile)

    args = {}
    # args.update(csrf(request))
    args.update(request)

    args['form'] = form
    return render_to_response('profile.html', args)
