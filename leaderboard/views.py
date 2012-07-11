from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response, render, redirect
from django.template import RequestContext
from django.utils import simplejson

from core.models import Ladder
from core.logic import get_ladder_or_404

from leaderboard.forms import SimpleMatchCreationForm
from leaderboard import logic
from leaderboard.models import Match

def leaderboard(request, ladder, form=None):
    if not form:
        form = SimpleMatchCreationForm()
    return render_to_response(
        'leaderboard/ladder.html',
        logic.get_ladder_context(ladder, {'form': form}),
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
        form = SimpleMatchCreationForm()
        form.success = "Match was created successfully"
        logic.adjust_rankings(match)
    return leaderboard(request, ladder, form=form)

def match(request, ladder_id, match_id):
    ladder = get_object_or_404(Ladder, pk=ladder_id)
    match = get_object_or_404(Match, pk=match_id)
    return render_to_response('leaderboard/match.html',
        {'ladder': ladder, 'match': match},
        context_instance=RequestContext(request)
    )

def ajax_match_creation(request, ladder_id):
    ladder = get_ladder_or_404(pk=ladder_id)
    if request.POST:
        form = SimpleMatchCreationForm(request.POST)
        if form.is_valid():
            match = form.save(commit=True)
            form = SimpleMatchCreationForm()
            form.success = "Match was created successfully"
            logic.adjust_rankings(match)
            if request.is_ajax():
                return render(request, 'leaderboard/match_entry_form.html', {'form': form, 'ladder': ladder})
            return redirect('ladders/{}'.format(ladder_id))
    else:
        form = SimpleMatchCreationForm()
    return render(request, 'leaderboard/match_entry_form.html', {'form': form, 'ladder': ladder})

def ajax_match_feed(request, ladder_id):
    match_feed = logic.get_match_feed(get_ladder_or_404(pk=ladder_id))
    return HttpResponse(simplejson.dumps(match_feed), mimetype='application/javascript')
