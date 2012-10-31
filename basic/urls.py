from django.conf.urls import patterns, url

urlpatterns = patterns('basic.views',
    url(r'^(?P<ladder_id>\d+)/$', 'ladder_page'),
    url(r'^(?P<ladder_id>\d+)/content/ladder_display/$', 'ladder_display'),
    url(r'^(?P<ladder_id>\d+)/configure/$', 'configure_ladder'),
    url(r'^(?P<ladder_id>\d+)/edit/$', 'edit_ladder'),
)
