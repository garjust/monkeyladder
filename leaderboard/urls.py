from django.conf.urls import patterns, url

urlpatterns = patterns('leaderboard.views',
    url(r'^(?P<ladder_id>\d+)/matches/$', 'matches'),
    url(r'^(?P<ladder_id>\d+)/matches/create/$', 'create_match'),
    url(r'^(?P<ladder_id>\d+)/matches/feed/$', 'ajax_match_feed'),
    url(r'^(?P<ladder_id>\d+)/matches/(?P<match_id>\d+)/$', 'match'),
)
