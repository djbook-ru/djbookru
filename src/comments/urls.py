from django.conf.urls.defaults import *

urlpatterns = patterns('comments.views',
    url('post/$', 'post', name='post'),
    url('update_comments/$', 'update_comments', name='update_comments'),
)