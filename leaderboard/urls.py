from django.conf.urls import patterns, url

urlpatterns = patterns('leaderboard.views',
    url(r'^matches/$', 'matches'),
    url(r'^matches/create/$', 'create_match'),
    url(r'^matches/feed/$', 'ajax_match_feed'),
    url(r'^matches/(?P<match_id>\d+)/$', 'match'),
)
