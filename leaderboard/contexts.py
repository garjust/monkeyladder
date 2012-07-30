from leaderboard.forms import MatchCreationForm, AdvancedMatchCreationForm, LeaderboardConfigurationForm
from leaderboard import logic

def view_ladder_context(request, ladder):
    games = request.GET.get('games', None)
    form = MatchCreationForm(ladder)
    if games:
        form = AdvancedMatchCreationForm(games, ladder)
    return {
        'player_names': ','.join(map(lambda n: '"%s"' % n, logic.get_ladder_players(ladder))),
        'match_feed': logic.get_match_feed(ladder),
        'form': form,
    }

def ladder_display_context(request, ladder):
    return {}