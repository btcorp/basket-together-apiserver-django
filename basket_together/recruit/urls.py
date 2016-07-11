"""basket_together URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from recruit.views import post_list

urlpatterns = [
    # url(r'^$', 'recruit.views.post_list', name='post_list'),
    url(r'^posts/$', 'recruit.views.post_list', name='post_list'),
    url(r'^post/add/$', 'recruit.views.post_add', name='post_add'),
    url(r'^post/(?P<pk>\d+)/$', 'recruit.views.post_detail', name='post_detail'),
    url(r'^post/(?P<pk>\d+)/edit/$', 'recruit.views.post_edit', name='post_edit'),
    url(r'^post/(?P<pk>\d+)/remove/$', 'recruit.views.post_remove', name='post_remove'),
    url(r'^post/(?P<pk>\d+)/comment/$', 'recruit.views.add_comment_to_post', name='add_comment_to_post'),
    url(r'^search/$', 'recruit.views.post_search', name='post_search'),
    url(r'^comment/(?P<pk>\d+)/remove/$', 'recruit.views.comment_remove', name='comment_remove'),
]
