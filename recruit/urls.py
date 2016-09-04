from django.conf.urls import url
from recruit import views

urlpatterns = [
    # url(r'^$', 'recruit.views.post_list', name='post_list'),
    url(r'^posts/$', views.post_list_all, name='post_list_all'),
    url(r'^posts/page-(?P<page>\d+)/$', views.post_list, name='post_list'),
    url(r'^post/add/$', views.post_add, name='post_add'),
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^post/(?P<pk>\d+)/comment/add/$', views.add_comment_to_post, name='add_comment_to_post'),
    url(r'^comment/(?P<pk>\d+)/remove/$', views.comment_remove, name='comment_remove'),
    url(r'^post/(?P<pk>\d+)/comments/$', views.comments_to_post, name='comments_to_post'),
    url(r'^post/(?P<pk>\d+)/participation/add/$', views.add_participation, name='add_participation'),
    url(r'^post/(?P<pk>\d+)/participation/remove/$', views.remove_participation, name='remove_participation'),
    url(r'^search/$', views.post_search, name='post_search'),
]
