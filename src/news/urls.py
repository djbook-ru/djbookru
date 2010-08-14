from django.conf.urls.defaults import *

urlpatterns = patterns('news.views',
    url(r'^$', 'index', name='index'),
    url(r'^(?P<pk>\d+)/$', 'news', name='news'),
)