from django.conf.urls import patterns, url

urlpatterns = patterns('leaderboard.views',
    url(r'^(?P<ladder_id>\d+)/$', 'ladder_page'),
    url(r'^(?P<ladder_id>\d+)/content/ladder_display/$', 'ladder_display'),
    url(r'^(?P<ladder_id>\d+)/configure/$', 'configure_ladder_page'),
    url(r'^(?P<ladder_id>\d+)/edit/$', 'edit_ladder'),
    url(r'^(?P<ladder_id>\d+)/matches/$', 'matches_page', name='matches_page'),
    url(r'^(?P<ladder_id>\d+)/matches/create/$', 'create_match', name='create_match'),

    url(r'^content/matches/$', 'matches'),
    url(r'^content/matches/(?P<match_id>\d+)$', 'match'),
    url(r'^content/stats/$', 'stats'),
    url(r'^content/matchups/$', 'matchups'),
)
