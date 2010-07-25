from django.conf.urls.defaults import *

urlpatterns = patterns('accounts.views',
    url('^login/$', 'login', name='login'),
    url('^logout/$', 'logout', name='logout'),
)