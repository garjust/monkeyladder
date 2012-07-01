from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from core.models import Ladder

from matches.logic import MatchCreator

@login_required(login_url="/accounts/login")
def matches(request, ladder_id):
    ladder = get_object_or_404(Ladder, pk=ladder_id)
    if request.POST:
        return _create_match(request, ladder)
    return _view_matches(request, ladder)  
    
def _view_matches(request, ladder):
    matches = ladder.matches()
    return render_to_response('ladders/matches.html',
        {'navbar_active': 'matches', 'ladder': ladder, 'matches': matches},
        context_instance=RequestContext(request)
    )

def _create_match(request, ladder):
    player_one = (request.POST['match-first-player-name'], request.POST['match-first-player-score'])
    player_two = (request.POST['match-second-player-name'], request.POST['match-second-player-score'])
    messages = {}
    try:
        messages['site_error_message'] = MatchCreator(ladder).create(player_one, player_two)
        messages['success_message'] = "Match was created successfully"
    except AssertionError as e:
        messages['site_error_message'] = str(e)
    return render_to_response('ladders/ladder.html',
        _get_context(ladder, messages),
        context_instance=RequestContext(request)
    )
    
def _get_context(ladder, messages):
    context = {'navbar_active': 'ladder', 'ladder': ladder}
    context.update(messages)
    return context 