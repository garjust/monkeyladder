from django.conf.urls import patterns, url

urlpatterns = patterns('basic.views',
    url(r'^$', 'view_ladder'),
    url(r'^content/ladder_display/$', 'ladder_display'),
    url(r'^configure/$', 'configure_ladder'),
    url(r'^edit/$', 'edit_ladder'),
)
