from django.conf.urls import patterns, url

urlpatterns = patterns('leaderboard.views',
    url(r'^configure/$', 'configure_ladder', name='configure_ladder'),
    url(r'^matches/$', 'view_matches', name='view_matches'),
    url(r'^matches/create/$', 'create_match'),
    url(r'^content/match_feed/$', 'match_feed_content', name="match_feed"),
)
