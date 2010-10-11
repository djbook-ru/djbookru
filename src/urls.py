from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
from patch import sites_flatpages_patch

admin.autodiscover()
sites_flatpages_patch()

js_info_dict = {
    'packages': ('main'),
}

urlpatterns = patterns('',
    (r'^', include('main.urls', 'main')),
    url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict, name='js_i18n_catalog'),
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
    
from django import http
from django.template import RequestContext, loader

def handler500(request, template_name='500.html'):
    print 'XYU'
    t = loader.get_template(template_name)
    return http.HttpResponseServerError(t.render(RequestContext(request)))