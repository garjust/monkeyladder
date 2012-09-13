from leaderboard.forms import LeaderboardConfigurationForm, get_match_form
from leaderboard import logic
from core.logic import get_base_ladder_context

def get_leaderboard_ladder_context(request, ladder, form=None):
    return get_base_ladder_context(request, ladder, extra=view_ladder_context(request, ladder, form))

def view_ladder_context(request, ladder, form=None):
    return {
        'player_names': logic.rankings.get_ladder_players_for_match_entry(ladder),
        'match_feed': logic.feeds.get_match_feed(ladder),
        'form': form if form else get_match_form(ladder, number_of_games=request.GET.get('games')),
    }

def ladder_display_context(request, ladder):
    return {}
