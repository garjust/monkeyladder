from django.conf.urls import patterns, include, url

urlpatterns = patterns('django.views.generic.simple',
    url(r'^$', 'redirect_to', {'url': '/ladders/home'}),
)

urlpatterns += patterns('ladders.views',
    url(r'^home$', 'home'),
    url(r'^watched$', 'watched'),
    url(r'^climbing$', 'climbing'),
    url(r'^(?P<ladder_id>\d+)/$', 'ladder'),
    url(r'^(?P<ladder_id>\d+)/update/$', 'update'),
    url(r'^(?P<ladder_id>\d+)/matches/$', 'matches'),
)