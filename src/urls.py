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
    url(r'^(?P<path>pics/.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )

from django.contrib.sitemaps import Sitemap, FlatPageSitemap, GenericSitemap
from dinette import models as d_models
from examples import models as r_models
from news import models as n_models
from comments import models as c_models

sitemap_dinette_topics = {
    'queryset': d_models.Ftopics.objects.filter(is_hidden=False),
    'date_field': 'updated_on',
    }
sitemap_dinette_replies = {
    'queryset': d_models.Reply.objects.filter(topic__is_hidden=False),
    'date_field': 'updated_on',
    }
sitemap_recipes = {
    'queryset': r_models.Example.objects.all(),
    'date_field': 'created',
    }
sitemap_news = {
    'queryset': n_models.News.objects.all(),
    'date_field': 'created',
    }
sitemap_comments = {
    'queryset': c_models.Comment.objects.all(),
    'date_field': 'submit_date',
    }
sitemaps = {
    'flatpages': FlatPageSitemap,
    'forum_topics': GenericSitemap(sitemap_dinette_topics, priority=0.5),
    'forum_topics': GenericSitemap(sitemap_dinette_replies, priority=0.5),
    'recipes': GenericSitemap(sitemap_recipes, priority=0.5),
    'news': GenericSitemap(sitemap_news, priority=0.5),
    'comment': GenericSitemap(sitemap_comments, priority=0.5),
    }
urlpatterns += patterns(
    '',
    (r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    (r'^robots.txt$', include('robots.urls')),
)

from django import http
from django.template import RequestContext, loader

def handler500(request, template_name='500.html'):
    t = loader.get_template(template_name)
    return http.HttpResponseServerError(t.render(RequestContext(request)))
