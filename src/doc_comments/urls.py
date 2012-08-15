from django.views.generic.simple import direct_to_template
from django.conf.urls.defaults import *

urlpatterns = patterns('doc_comments.views',
    url(r'^add/$', 'add', name='add'),
    url(r'^get_login_status/$', 'get_login_status', name='get_login_status'),
    url(r'^load_comments/$', 'load_comments', name='load_comments'),
    url(r'^load_comments_info/$', 'load_comments_info', name='load_comments_info')
)
