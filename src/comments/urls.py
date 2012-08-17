# -*- coding: utf-8 -*-

from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('src.comments.views',
    url('post/$', 'post', name='post'),
    url('update_comments/$', 'update_comments', name='update_comments'),
)
