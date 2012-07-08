from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from core.models import Ladder

from leaderboard.logic import MatchCreator, RankingAlgorithm, get_ladder_context
from leaderboard.models import Match

def leaderboard(request, ladder):
    return render_to_response(
        'matches/ladder.html',
        get_ladder_context(ladder),
        context_instance=RequestContext(request),
    )

def matches(request, ladder_id):
    ladder = get_object_or_404(Ladder, pk=ladder_id)
    if request.POST:
        return _create_match(request, ladder)
    return _view_matches(request, ladder)
    
def _view_matches(request, ladder):
    matches = ladder.match_set.filter().order_by('-match_date')
    return render_to_response('matches/match_history.html',
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
        RankingAlgorithm().adjust_rankings(match)
    except AssertionError as e:
        messages['site_error_message'] = str(e)
        messages['error_message'] = str(e)
    return render_to_response('matches/ladder.html',
        get_ladder_context(ladder, messages),
        context_instance=RequestContext(request)
    )
    
def match(request, ladder_id, match_id):
    ladder = get_object_or_404(Ladder, pk=ladder_id)
    match = get_object_or_404(Match, pk=match_id)
    if request.POST:
        return _create_comment(request, ladder, match)
    return _view_match(request, ladder, match)

def _view_match(request, ladder, match):
    return render_to_response('matches/match.html',
        {'ladder': ladder, 'match': match},
        context_instance=RequestContext(request)
    )

@login_required(login_url="/accounts/login")
def _create_comment(request, ladder, match):
    user = request.user
    comment = (request.POST['comment'])
    return render_to_response('matches/match.html',
        {'ladder': ladder, 'match': match},
        context_instance=RequestContext(request)
    )