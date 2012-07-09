from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from core.models import Ladder

from leaderboard.forms import SimpleMatchCreationForm
from leaderboard.logic import MatchCreator, get_ladder_context, adjust_rankings
from leaderboard.models import Match

def leaderboard(request, ladder):
    return render_to_response(
        'leaderboard/ladder.html',
        get_ladder_context(ladder),
        context_instance=RequestContext(request),
    )

def matches(request, ladder_id):
    ladder = get_object_or_404(Ladder, pk=ladder_id)
    if request.POST:
        return _create_match(request, ladder)
    return _view_matches(request, ladder)
    
def _view_matches(request, ladder):
    matches = ladder.match_set.filter().order_by('-created')
    return render_to_response('leaderboard/match_history.html',
        {'navbar_active': 'matches', 'ladder': ladder, 'matches': matches},
        context_instance=RequestContext(request)
    )

@login_required(login_url="/accounts/login")
def _create_match(request, ladder):
    player_one = (request.POST['match-first-player-name'], request.POST['match-first-player-score'])
    player_two = (request.POST['match-second-player-name'], request.POST['match-second-player-score'])
    messages = {}
    try:
        match = MatchCreator(ladder).create(request.user, player_one, player_two)
        messages['success_message'] = "Match was created successfully"
        adjust_rankings(match)
    except AssertionError as e:
        messages['site_error_message'] = str(e)
        messages['error_message'] = str(e)
    return render_to_response('leaderboard/ladder.html',
        get_ladder_context(ladder, messages),
        context_instance=RequestContext(request)
    )
    
def match(request, ladder_id, match_id):
    ladder = get_object_or_404(Ladder, pk=ladder_id)
    match = get_object_or_404(Match, pk=match_id)
    return render_to_response('leaderboard/match.html',
        {'ladder': ladder, 'match': match},
        context_instance=RequestContext(request)
    )
    