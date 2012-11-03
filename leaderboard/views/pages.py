from core.decorators import can_view_ladder, login_required_and_ladder_admin, ladder_is_active
from core.generic_views import handle_form_and_redirect_to_ladder, view_with_ladder
from core.logic.util import get_ladder_or_404
from leaderboard.forms import LeaderboardConfigurationForm
from leaderboard.generic_views import view_with_leaderboard


@can_view_ladder
def matches_page(request, ladder_id):
    ladder = get_ladder_or_404(pk=ladder_id)
    match_id = request.GET.get('id', None)
    return view_with_ladder(request, ladder, 'leaderboard/matches_page.html', {
        'navbar_active': 'matches', 'match_id': match_id, 'match_feed_size': 10,
    })


@ladder_is_active
@can_view_ladder
def ladder_page(request, ladder_id):
    ladder = get_ladder_or_404(pk=ladder_id)
    return view_with_leaderboard(request, ladder, 'leaderboard/ladder_page.html', {'navbar_active': 'ladder'})


@ladder_is_active
@login_required_and_ladder_admin
def configure_ladder_page(request, ladder_id):
    return handle_form_and_redirect_to_ladder(request, ladder_id, LeaderboardConfigurationForm, 'leaderboard/configure_ladder_page.html',
        context={'navbar_active': 'config'}
    )
