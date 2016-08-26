from accounts.models import UserProfile
from django import forms


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('phone_number', 'device_type',)
