from django.conf.urls import patterns, url

urlpatterns = patterns('django.views.generic.simple',
    url(r'^$', 'redirect_to', {'url': '/ladders/home'}),
)

urlpatterns += patterns('core.views',
    url(r'^create/$', 'create'),
    url(r'^activity/$', 'activity'),
    url(r'^(?P<ladder_id>\d+)/$', 'ladder'),
    url(r'^(?P<ladder_id>\d+)/watchers/$', 'watchers'),
)