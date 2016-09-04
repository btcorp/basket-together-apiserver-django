# -*- coding:utf-8 -*-

import re
from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.shortcuts import get_list_or_404

DEVICE_TYPE=(
    ('a', 'ANDROID'),
    ('i', 'IOS'),
)


def phonenumber_validator(value):
    if re.match(r'^01[016789][1-9]\d{6,7}$', value) is None:
        raise ValidationError('휴대폰 번호를 입력해주세요.')


class PhoneNumberField(models.CharField):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 15)
        kwargs.setdefault('validators', [])
        kwargs['validators'].append(phonenumber_validator)
        super(PhoneNumberField, self).__init__(*args, **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = PhoneNumberField(max_length=12, blank=True)
    device_type = models.CharField(max_length=10, choices=DEVICE_TYPE, default='ANDROID')
    join_path = models.CharField(max_length=20, default='general')
    attend_count = models.IntegerField(blank=True, default=0)
    penalty_count = models.IntegerField(blank=True, default=0)
    user_image = models.ImageField(blank=True, upload_to='%Y/%m/%d')

    # class Meta:
    #     managed = False     # 자동으로 테이블을 생성하지 않게 된다

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    def as_json(self):
        return {
            'id': self.user.id,
            'name': self.user.username,
            'phone_number': self.phone_number,
            'device_type': self.device_type,
            'attend_count': self.attend_count,
            'penalty_count': self.penalty_count,
            # 'user_image': self.user_image
        }


class Friendship(models.Model):
    from_friend = models.ForeignKey(User, related_name='from_friends')
    to_friend = models.ForeignKey(User, related_name='to_friends')

    class Meta:
        # managed = False  # 자동으로 테이블을 생성하지 않게 된다
        unique_together = (('from_friend', 'to_friend'), )

    def __str__(self):
        return '{}, {}'.format(self.from_friend, self.to_friend)


User.profile = property(lambda user: Profile.objects.get_or_create(user=user)[0])

