from django.conf.urls import patterns, url

urlpatterns = patterns('leaderboard.views',
    url(r'^matches/$', 'matches'),
    url(r'^matches/create/$', 'create_match'),
    url(r'^content/match_feed/$', 'match_feed_content', name="match_feed"),
)
