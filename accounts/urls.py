from django.conf.urls import url
from accounts import views
from rest_framework.authtoken import views as rest_views

urlpatterns = [
    # url(r'^profile/$', 'accounts.views.accounts', name='accounts'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', views.login_view, name='login'),
    # url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^api-auth-token/$', rest_views.obtain_auth_token, name='get_auth_token'),
]