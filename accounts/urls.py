from django.conf.urls import url
from accounts import views
from rest_framework.authtoken import views as rest_views

urlpatterns = [
    url(r'^api-auth-token/$', rest_views.obtain_auth_token, name='get_auth_token'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', views.login_view, name='login'),
    # url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^profile/$', views.user_profile, name='user_profile'),
    url(r'^(?P<id>\d+)/picture/$', views.get_picture, name='get_picture'),
]
