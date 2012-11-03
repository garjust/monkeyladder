from core.generic_views import view_with_ladder

from leaderboard.forms import get_match_form
from leaderboard import logic


def view_with_leaderboard(request, ladder, template, context=None, form=None):
    if not context:
        context = {}
    context.update({
        'player_names': logic.rankings.get_ladder_players_for_match_entry(ladder),
        'form': form if form else get_match_form(ladder, number_of_games=request.GET.get('games')),
    })
    return view_with_ladder(request, ladder, template, context)
