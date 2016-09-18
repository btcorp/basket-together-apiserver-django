# -*- coding:utf-8 -*-

import ast
import json
from accounts.models import Profile
from accounts.forms import UserProfileForm, UserForm, SignupForm
from django.core.exceptions import ObjectDoesNotExist
from django.forms import model_to_dict
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response


# byte to string 헬퍼 메서드
def decoding_byte_to_string(request):
    bytes_to_string = (request.body).decode('utf-8')
    return json.loads(bytes_to_string)


# token 값으로 유저 출력
def get_user_in_token(request):
    token_ = Token.objects.get(pk=request.META.get('HTTP_TOKEN'))
    return token_.user


def output_message_json(message, status=None):
    return JsonResponse(
        {'message': message},
        json_dumps_params={'ensure_ascii': False},
        safe=False,
        status=status
    )


@csrf_exempt
def signup(request):
    data = decoding_byte_to_string(request)
    form = SignupForm(data)
    if form.is_valid():
        user = form.save()
        profile = user.get_profile()
        profile.nickname = data.get('nickname')
        profile.save()
        user_dict = model_to_dict(user, fields=['id', 'username'])
        return JsonResponse(user_dict)
    return JsonResponse(form.errors)


@csrf_exempt
def login_view(request):
    data = decoding_byte_to_string(request)
    username = data.get('username')
    password = data.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        try:
            user.auth_token.delete()
        except ObjectDoesNotExist:
            pass
        login(request, user)
        return create_auth_token(request)    # create token
    else:
        return output_message_json('ID 및 비밀번호가 존재하지 않습니다.')


@csrf_exempt
def user_profile(request):
    """
    Form to update User profile
    """
    user_ = get_user_in_token(request)

    if request.method == 'POST':
        data = decoding_byte_to_string(request)
        profileForm = UserProfileForm(data, instance=user_.get_profile())
        userForm = UserForm(data, instance=user_)
        if profileForm.is_valid() and userForm.is_valid():
            profileForm.save()
            userForm.save()
            return output_message_json('프로필이 변경 되었습니다.', 201)
    else:
        profileForm = UserProfileForm(instance=user_.get_profile())
        userForm = UserForm(instance=user_)

    return userForm.instance


class CreateAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user_id': user.id, 'nickname': user.get_profile().nickname})

create_auth_token = CreateAuthToken.as_view()
