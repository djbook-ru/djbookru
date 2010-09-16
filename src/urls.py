from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
from patch import sites_flatpages_patch

admin.autodiscover()
sites_flatpages_patch()

urlpatterns = patterns('',
    (r'^', include('main.urls', 'main')),
    (r'^news/', include('news.urls', 'news')),
    (r'^claims/', include('claims.urls', 'claims')),
    (r'^examples/', include('examples.urls', 'examples')),
    (r'auth/', include('accounts.urls', 'accounts')),
    (r'socialauth/', include('socialauth.urls')),
    (r'forum/', include('dinette.urls')),
    (r'^grappelli/', include('grappelli.urls')),
    (r'^admin_tools/', include('admin_tools.urls')),
    (r'^admin/filebrowser/', include('filebrowser.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^comments/', include('comments.urls', 'comments')),    
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )