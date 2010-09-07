from django.conf.urls.defaults import *

urlpatterns = patterns('examples.views',
    url(r'^$', 'index', name='index'),
    url(r'^(?P<pk>\d+)/$', 'detail', name='detail'),
    url(r'^c(?P<pk>\d+)/$', 'category', name='category'),
)