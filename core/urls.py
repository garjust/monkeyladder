from django.conf.urls import patterns, url

urlpatterns = patterns('django.views.generic.simple',
    url(r'^$', 'redirect_to', {'url': '/ladders/feeds/'}),
)

urlpatterns += patterns('core.views',
    url(r'^feeds/$', 'feeds'),
    url(r'^create/$', 'create_ladder', name='create_ladder'),
    url(r'^(?P<ladder_id>\d+)/watch/$', 'watch_ladder', name='watch_ladder'),
    url(r'^(?P<ladder_id>\d+)/delete/$', 'delete_ladder', name='delete_ladder'),
)
