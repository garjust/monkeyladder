from leaderboard.forms import LeaderboardConfigurationForm, get_match_form
from leaderboard import logic

def view_ladder_context(request, ladder):
    return {
        'player_names': ','.join(map(lambda n: '"%s"' % n, logic.get_ladder_players(ladder))),
        'match_feed': logic.get_match_feed(ladder),
        'form': get_match_form(ladder, games=request.GET.get('games')),
    }

def ladder_display_context(request, ladder):
    return {}
