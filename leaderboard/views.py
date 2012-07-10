from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from core.models import Ladder

from leaderboard.forms import SimpleMatchCreationForm
from leaderboard.logic import get_ladder_context, adjust_rankings
from leaderboard.models import Match

def leaderboard(request, ladder, form=None):
    if not form:
        form = SimpleMatchCreationForm()
    return render_to_response(
        'leaderboard/ladder.html',
        get_ladder_context(ladder, {'form': form}),
        context_instance=RequestContext(request),
    )

def matches(request, ladder_id):
    ladder = get_object_or_404(Ladder, pk=ladder_id)
    if request.POST:
        return _create_match(request, ladder)
    matches = ladder.match_set.filter().order_by('-created')
    return render_to_response('leaderboard/match_history.html',
        {'navbar_active': 'matches', 'ladder': ladder, 'matches': matches},
        context_instance=RequestContext(request)
    )

@login_required(login_url="/accounts/login")
def _create_match(request, ladder):
    form = SimpleMatchCreationForm(request.POST)
    if form.is_valid():
        match = form.save(commit=True)
        #next = form.cleaned_data['next']
        form = SimpleMatchCreationForm()
        form.success = "Match was created successfully"
        #form.next = next
        #form.cleaned_data['next'] = next
        adjust_rankings(match)
    return leaderboard(request, ladder, form=form)
    #return HttpResponseRedirect(form.cleaned_data['next'])
    
def match(request, ladder_id, match_id):
    ladder = get_object_or_404(Ladder, pk=ladder_id)
    match = get_object_or_404(Match, pk=match_id)
    return render_to_response('leaderboard/match.html',
        {'ladder': ladder, 'match': match},
        context_instance=RequestContext(request)
    )
    