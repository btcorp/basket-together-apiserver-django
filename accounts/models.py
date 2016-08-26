from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=12)
    device_type = models.CharField(max_length=1, default='a')
    join_path = models.CharField(max_length=20, default='general')
    attend_count = models.IntegerField(blank=True, default=0)
    penalty_count = models.IntegerField(blank=True, default=0)


User.profile = property(lambda user: UserProfile.objects.get_or_create(user=user)[0])

