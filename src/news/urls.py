from django.conf.urls.defaults import *

urlpatterns = patterns('news.views',
    url(r'^$', 'index', name='index'),
)