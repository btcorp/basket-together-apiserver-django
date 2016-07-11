from django.conf.urls import url
from user_profile import views

urlpatterns = [
    # url(r'^profile/$', 'user_profile.views.user_profile', name='user_profile'),
    url(r'^signup/$', views.signup, name='signup'),
    # url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),
    # url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', name='logout'),
]
