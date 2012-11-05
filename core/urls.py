from django.conf.urls import patterns, url

urlpatterns = patterns('django.views.generic.simple',
    url(r'^$', 'redirect_to', {'url': '/ladders/feeds/'}),
)

urlpatterns += patterns('core.views',
    url(r'^feeds/$', 'ladder_feeds_page'),
    url(r'^create/$', 'create_ladder_page'),
    url(r'^(?P<ladder_id>\d+)/watch/$', 'watch_ladder', name='watch_ladder'),
    url(r'^(?P<ladder_id>\d+)/delete/$', 'delete_ladder', name='delete_ladder'),
)
