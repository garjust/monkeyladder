from django.conf.urls import patterns, url

urlpatterns = patterns('leaderboard.views',
    url(r'^matches/$', 'view_matches', name='view_matches'),
    url(r'^matches/create/$', 'create_match', name='create_match'),
    url(r'^content/match_feed/$', 'match_feed_content', name="match_feed"),
    url(r'^$', 'view_ladder'),
    url(r'^content/ladder_display/$', 'ladder_display', name='leaderboard-ladder-display'),
    url(r'^configure/$', 'configure_ladder'),
    url(r'^edit/$', 'edit_ladder'),
)
