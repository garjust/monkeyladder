from django.conf.urls import patterns, url

urlpatterns = patterns('matches.views',
    url(r'^(?P<ladder_id>\d+)/matches$', 'matches'),
)