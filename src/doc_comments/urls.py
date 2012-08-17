# -*- coding: utf-8 -*-

from django.conf.urls.defaults import  url, patterns

urlpatterns = patterns('src.doc_comments.views',
    url(r'^add/$', 'add', name='add'),
    url(r'^close_comment/$', 'close_comment', name='close_comment'),
    url(r'^accept_comment/$', 'accept_comment', name='accept_comment'),
    url(r'^get_login_status/$', 'get_login_status', name='get_login_status'),
    url(r'^load_comments/$', 'load_comments', name='load_comments'),
    url(r'^load_comments_info/$', 'load_comments_info', name='load_comments_info')
)
