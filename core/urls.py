from django.conf.urls import patterns, url

urlpatterns = patterns('django.views.generic.simple',
    url(r'^$', 'redirect_to', {'url': '/ladders/activity/'}),
)

urlpatterns += patterns('core.delegator',
    url(r'^(?P<ladder_id>\d+)/$', 'delegate_ladder_view', name='view_ladder'),
    url(r'^(?P<ladder_id>\d+)/edit/$', 'delegate_ladder_edit', name='edit_ladder'),
    url(r'^(?P<ladder_id>\d+)/watchers/$', 'delegate_watchers_view', name='view_ladder_watchers'),
    url(r'^(?P<ladder_id>\d+)/content/ladder_display/$', 'delegate_ladder_content', name='ladder_display_content'),             
)

urlpatterns += patterns('core.views',
    url(r'^activity/$', 'feeds'),
    url(r'^create/$', 'create_ladder', name='create_ladder'),    
)