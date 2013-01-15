from django.conf.urls import patterns, include, url


urlpatterns = patterns('src.code_review.views',
    url(r'^$', 'index', name='index'),
    url(r'^comments_api/(?P<file_id>\d+)/$', 'comments_api', name='comments_api'),
    url(r'^details/(\d+)/$', 'details', name='details'),
)
