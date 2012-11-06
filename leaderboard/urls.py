from django.conf.urls import patterns, url

urlpatterns = patterns('leaderboard.views.pages',
    url(r'^(?P<ladder_id>\d+)/$', 'ladder_page'),
    url(r'^(?P<ladder_id>\d+)/matches/$', 'matches_page'),
    url(r'^(?P<ladder_id>\d+)/configure/$', 'configure_ladder_page'),
)

urlpatterns += patterns('leaderboard.views.content',
    url(r'^(?P<ladder_id>\d+)/display/$', 'display_ladder'),
    url(r'^(?P<ladder_id>\d+)/edit/$', 'edit_ladder'),
    url(r'^(?P<ladder_id>\d+)/matches/create/$', 'create_match'),
    url(r'^content/matches/$', 'matches'),
    url(r'^content/matches/(?P<match_id>\d+)$', 'match'),
    url(r'^content/stats/$', 'stats'),
    url(r'^content/matchups/$', 'matchups'),
)
