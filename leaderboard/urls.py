from django.conf.urls import patterns, url

urlpatterns = patterns('leaderboard.views',
    url(r'^(?P<ladder_id>\d+)/matches/$', 'matches'),
    url(r'^(?P<ladder_id>\d+)/matches/(?P<match_id>\d+)/$', 'match'),
)