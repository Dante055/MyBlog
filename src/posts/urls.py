from django.conf.urls import url

from .views import (
    post_list,
    post_create,
    post_detail,
    post_update,
    post_delete,
    PostLikeToggle,
    PostDislikeToggle,
)

urlpatterns = [
    url(r'^$', post_list, name='list'),
    url(r'^create/$', post_create, name='create'),
    url(r'^(?P<slug>[\w-]+)/$', post_detail, name='detail'),
    url(r'^(?P<slug>[\w-]+)/edit/$', post_update, name='update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', post_delete, name='delete'),
    url(r'^(?P<slug>[\w-]+)/like/$', PostLikeToggle.as_view(), name='like-toggle'),
    url(r'^(?P<slug>[\w-]+)/dislike/$', PostDislikeToggle.as_view(), name='dislike-toggle')
    # url(r'^posts/$', "<appname>.views.<function_name>"),
]
