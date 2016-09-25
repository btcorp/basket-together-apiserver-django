# -*- coding:utf-8 -*-

import re
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import ASCIIUsernameValidator, UnicodeUsernameValidator
from django.db import models
from django.forms import ValidationError
from django.utils import six, timezone
from django.utils.translation import ugettext_lazy as _


def phonenumber_validator(value):
    if re.match(r'^01[016789][1-9]\d{6,7}$', value) is None:
        raise ValidationError('휴대폰 번호를 입력해주세요.')


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user/{0}/{1}'.format(instance.user.id, filename)


class PhoneNumberField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 15)
        kwargs.setdefault('help_text', "'-' 없이 번호를 입력해주세요.")
        kwargs.setdefault('validators', [])
        kwargs['validators'].append(phonenumber_validator)
        super(PhoneNumberField, self).__init__(*args, **kwargs)


class Profile(models.Model):
    DEVICE_TYPE = (
        ('a', 'ANDROID'),
        ('i', 'IOS'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=200, blank=True)
    phone_number = PhoneNumberField(max_length=12, blank=True)
    device_type = models.CharField(max_length=10, choices=DEVICE_TYPE, default='ANDROID')
    join_path = models.CharField(max_length=20, default='general')
    attend_count = models.IntegerField(blank=True, default=0)
    penalty_count = models.IntegerField(blank=True, default=0)
    user_image = models.ImageField(blank=True, upload_to=user_directory_path)

    # class Meta:
    #     managed = False     # 자동으로 테이블을 생성하지 않게 된다

    def __str__(self):  # __unicode__ on Python 2
        return self.user.username

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    def as_json(self):
        return {
            'user_id': self.user.id,
            'nickname': self.nickname,
            'user_name': self.user.username,
            'email': self.user.email,
            'phone_number': self.phone_number,
            'device_type': self.device_type,
            'attend_count': self.attend_count,
            'penalty_count': self.penalty_count,
            # 'user_image': self.user_image
        }


class Friendship(models.Model):
    from_friend = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='from_friends')
    to_friend = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='to_friends')

    class Meta:
        # managed = False
        unique_together = (('from_friend', 'to_friend'), )

    def __str__(self):
        return '{}, {}'.format(self.from_friend, self.to_friend)


class ExtendedUser(AbstractUser):
    username_validator = UnicodeUsernameValidator() if six.PY3 else ASCIIUsernameValidator()

    username = models.CharField(
        _('Username or Email'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    # class Meta:
    #     managed = False

    def get_profile(self):
        return self.profile

    def save(self, *args, **kwargs):
        is_new = self.id is None
        super(ExtendedUser, self).save(*args, **kwargs)
        if is_new:
            Profile.objects.create(user=self)

    def as_json(self):
        return {
            'user_id': self.id,
            'user_name': self.username,
            'email': self.email,
        }


ExtendedUser.profile = property(lambda user: Profile.objects.get_or_create(user=user)[0])

