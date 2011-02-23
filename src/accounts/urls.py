from django.conf.urls.defaults import *
from django.contrib.auth.views import login

urlpatterns = patterns('',
    url('^login/$', login, name='login'),
)

urlpatterns += patterns('accounts.views',
    url('^slogin/$', 'slogin', name='slogin'),
    url('^logout/$', 'logout', name='logout'),
    url('^edit/$', 'edit', name='edit'),
    url('^create/$', 'create', name='create'),
    url('^(?P<pk>\d+)/$', 'profile', name='profile')
)

