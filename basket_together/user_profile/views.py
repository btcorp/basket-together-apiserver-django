from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, JsonResponse
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from django.contrib.auth.forms import UserCreationForm
from django.forms import model_to_dict
from django.views.decorators.csrf import csrf_exempt
import ast


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
    args.update(csrf(request))

    args['form'] = form
    return render_to_response('profile.html', args)


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

