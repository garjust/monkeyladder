from django.conf.urls import patterns, url

urlpatterns = patterns('leaderboard.views',
    url(r'^(?P<ladder_id>\d+)/matches/$', 'view_matches', name='view_matches'),
    url(r'^(?P<ladder_id>\d+)/matches/create/$', 'create_match', name='create_match'),
    url(r'^(?P<ladder_id>\d+)/$', 'view_ladder'),
    url(r'^(?P<ladder_id>\d+)/content/ladder_display/$', 'ladder_display', name='leaderboard-ladder-display'),
    url(r'^(?P<ladder_id>\d+)/configure/$', 'configure_ladder'),
    url(r'^(?P<ladder_id>\d+)/edit/$', 'edit_ladder'),
    url(r'^content/matchup/$', 'matchup'),
    url(r'^content/matches/$', 'matches'),
    url(r'^content/stats/$', 'stats'),
)
