from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response, render, redirect
from django.template import RequestContext

from core.models import Ladder
from core.logic import get_ladder_or_404
from accounts.decorators import login_required_forbidden

from leaderboard.forms import MatchCreationForm, AdvancedMatchCreationForm
from leaderboard import logic

def leaderboard(request, ladder, form=None):
    games = request.GET.get('games', None)
    if not form:
        form = MatchCreationForm()
    if games:
        form = AdvancedMatchCreationForm(int(games))
    return render_to_response(
        'leaderboard/full/ladder.html',
        logic.get_ladder_context(ladder, {'form': form, 'games': games}),
        context_instance=RequestContext(request),
    )

def matches(request, ladder_id):
    ladder = get_object_or_404(Ladder, pk=ladder_id)
    matches = ladder.match_set.filter().order_by('-created')
    match_id = request.GET.get('id', None)
    return render_to_response('leaderboard/full/match_history.html',
        {'navbar_active': 'matches', 'ladder': ladder, 'matches': matches, 'match_id': match_id},
        context_instance=RequestContext(request)
    )

@login_required_forbidden
def create_match(request, ladder_id):
    ladder = get_ladder_or_404(pk=ladder_id)
    if request.POST:
        if request.GET.get('games', None):
            form = AdvancedMatchCreationForm(int(request.GET.get('games')), request.POST)
        else:
            form = MatchCreationForm(request.POST)
        if form.is_valid():
            match = form.save(commit=True)
            form = MatchCreationForm()
            form.success = "Match was created successfully"
            logic.adjust_rankings(match)
            if request.is_ajax():
                return render(request, 'leaderboard/match_entry_form.html', {'form': form, 'ladder': ladder, 'new_match': match})
            return redirect('ladders/{}'.format(ladder_id))
    else:
        form = MatchCreationForm()
    return render(request, 'leaderboard/match_entry_form.html', {'form': form, 'ladder': ladder})

def ajax_ladder_display(request, ladder):
    return render(request, 'leaderboard/ladder_display.html', {'ladder': ladder})

def match_feed_content(request, ladder_id):
    match_feed = logic.get_match_feed(get_ladder_or_404(pk=ladder_id))
    return render(request, 'leaderboard/match_feed.html', {'match_feed': match_feed})
