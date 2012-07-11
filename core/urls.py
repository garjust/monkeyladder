from django.conf.urls import patterns, url

urlpatterns = patterns('django.views.generic.simple',
    url(r'^$', 'redirect_to', {'url': '/ladders/activity/'}),
)

urlpatterns += patterns('core.views',
    url(r'^activity/$', 'activity'),
    url(r'^create/$', 'create'),
    url(r'^content/ladder_creation_form/$', 'ladder_creation_form_content', name='ladder_creation_form'),
    url(r'^(?P<ladder_id>\d+)/$', 'ladder'),
    url(r'^(?P<ladder_id>\d+)/content/ladder_display/$', 'ladder_display_content', name='ladder_display'),
    url(r'^(?P<ladder_id>\d+)/watchers/$', 'watchers'),
)
