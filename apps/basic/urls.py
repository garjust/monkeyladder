from django.conf.urls import patterns, url

urlpatterns = patterns('basic.views.pages',
    url(r'^(?P<ladder_id>\d+)/$', 'ladder_page'),
    url(r'^(?P<ladder_id>\d+)/configure/$', 'configure_ladder_page'),
)

urlpatterns += patterns('basic.views.content',
    url(r'^(?P<ladder_id>\d+)/display/$', 'display_ladder'),
    url(r'^(?P<ladder_id>\d+)/edit/$', 'edit_ladder'),
)
