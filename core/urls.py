from django.conf.urls import patterns, url

urlpatterns = patterns('django.views.generic.simple',
    url(r'^$', 'redirect_to', {'url': '/ladders/feeds/'}),
)

urlpatterns += patterns('core.views',
    url(r'^feeds/$', 'feeds'),
    url(r'^create/$', 'create_ladder', name='create_ladder'),
    url(r'^(?P<ladder_id>\d+)/watch/$', 'watch_ladder', name='watch_ladder'),
    url(r'^basic/(?P<ladder_id>\d+)/$', 'view_ladder'),
    url(r'^basic/(?P<ladder_id>\d+)/content/ladder_display/$', 'ladder_display'),
    url(r'^basic/(?P<ladder_id>\d+)/configure/$', 'configure_ladder'),
    url(r'^basic/(?P<ladder_id>\d+)/edit/$', 'edit_ladder'),
)
