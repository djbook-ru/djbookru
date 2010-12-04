from django.conf.urls.defaults import *

urlpatterns = patterns('claims.views',
    url(r'^$', 'index', name='index'),
)
