# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from patch import sites_flatpages_patch

admin.autodiscover()
sites_flatpages_patch()

js_info_dict = {
    'packages': ('src.main', 'src'),
}

urlpatterns = patterns('',
    url(r'^', include('src.main.urls', 'main')),
    url(r'^', include('social_auth.urls')),
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^sentry/', include('sentry.urls')),
    url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict, name='js_i18n_catalog'),
    url(r'^adzone/', include('adzone.urls')),
    url(r'^news/', include('src.news.urls', 'news')),
    url(r'^videos/', include('src.videos.urls', 'videos')),
    url(r'^claims/', include('src.claims.urls', 'claims')),
    url(r'^review/', include('src.code_review.urls', 'code_review')),
    url(r'^examples/', include('src.examples.urls', 'examples')),
    url(r'^auth/', include('src.accounts.urls', 'accounts')),
    url(r'^forum/', include('src.forum.urls', 'forum')),
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^doc_comments/', include('src.doc_comments.urls', 'doc_comments')),
    url(r'^comments/', include('src.comments.urls', 'comments')),
    url(r'^tagging_autocomplete/', include('tagging_autocomplete.urls')),
    #url(r'^(?P<path>pics/.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )

# if settings.DEBUG:
#     urlpatterns += patterns('',
#         url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
#     )

from django.contrib.sitemaps import FlatPageSitemap, GenericSitemap
from . examples import models as r_models
from . news import models as n_models
from . forum import models as f_models

sitemap_forum = {
    'queryset': f_models.Topic.objects.all(),
    'date_field': 'created'
}
sitemap_recipes = {
    'queryset': r_models.Example.objects.all(),
    'date_field': 'created',
}
sitemap_news = {
    'queryset': n_models.News.objects.all(),
    'date_field': 'created',
}
sitemaps = {
    'flatpages': FlatPageSitemap,
    'recipes': GenericSitemap(sitemap_recipes, priority=0.5),
    'news': GenericSitemap(sitemap_news, priority=0.5),
    'forum': GenericSitemap(sitemap_forum, priority=0.5)
}

urlpatterns += patterns('',
    (r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    (r'^robots.txt$', include('robots.urls')),
)

from django import http
from django.template import RequestContext, loader


def handler500(request, template_name='500.html'):
    t = loader.get_template(template_name)
    return http.HttpResponseServerError(t.render(RequestContext(request)))
