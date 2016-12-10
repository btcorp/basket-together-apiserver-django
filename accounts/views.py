# -*- coding:utf-8 -*-

import ast
import json
import urllib
from accounts.models import Profile
from accounts.forms import UserProfileForm, UserForm, SignupForm
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.forms import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from basket_together.json_data_format import *


# token 값으로 유저 출력
def get_user_in_token(request):
    token_ = Token.objects.get(pk=request.META.get('HTTP_TOKEN'))
    return token_.user

@csrf_exempt
def signup(request):
    form = SignupForm(request.POST)
    if form.is_valid():
        user = form.save()
        profile = user.get_profile()
        profile.nickname = request.POST.get('nickname')
        profile.save()
        user_dict = model_to_dict(user, fields=['id', 'username'])
        return JsonResponse(user_dict)
    return JsonResponse(form.errors)


@csrf_exempt
def login_view(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        try:
            user.auth_token.delete()
        except ObjectDoesNotExist:
            pass
        login(request, user)
        return create_auth_token(request)    # create token
    else:
        return output_format_json_response(message='ID 및 비밀번호가 존재하지 않습니다.')


@csrf_exempt
def logout_view(request):
    logout(request);
    return output_format_json_response(statusCode=0000)


@csrf_exempt
def user_profile(request):
    """
    Form to update User profile
    """
    user_ = get_user_in_token(request)

    if request.method == 'POST':
        nic = request.POST.get('nicname')
        profileForm = UserProfileForm(request.POST, request.FILES, instance=user_.get_profile())
        userForm = UserForm(request.POST, instance=user_)
        # if profileForm.is_valid() and userForm.is_valid():
        if profileForm.is_valid():
            profileForm.save()
            userForm.save()
            return output_format_json_response(201, message='프로필이 변경 되었습니다.', statusCode='0000')
    else:
        profile = request.user.get_profile()
        profile_data = {
            'nickname': profile.nickname,
            'picture_url': profile.get_image_url(),
            'phone_number': profile.phone_number
        }
        return output_format_response(200, statusCode='0000', data=profile_data)

    return output_format_json_response(message='요청이 잘못되었습니다.', statusCode='5555')


class CreateAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        user_data = {
            'token': token.key,
            'user_id': user.id,
            'nickname': user.get_profile().nickname,
            'picture_url': user.profile.get_image_url(),
        }
        return output_format_response(200, statusCode='0000', data=user_data)

create_auth_token = CreateAuthToken.as_view()
