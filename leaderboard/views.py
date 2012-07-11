from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response, render, redirect
from django.template import RequestContext

from core.models import Ladder
from core.logic import get_ladder_or_404

from leaderboard.forms import MatchCreationForm
from leaderboard import logic
from leaderboard.models import Match

def leaderboard(request, ladder, form=None):
    if not form:
        form = MatchCreationForm()
    return render_to_response(
        'leaderboard/ladder.html',
        logic.get_ladder_context(ladder, {'form': form}),
        context_instance=RequestContext(request),
    )

def matches(request, ladder_id):
    ladder = get_object_or_404(Ladder, pk=ladder_id)
    matches = ladder.match_set.filter().order_by('-created')
    return render_to_response('leaderboard/match_history.html',
        {'navbar_active': 'matches', 'ladder': ladder, 'matches': matches},
        context_instance=RequestContext(request)
    )

def match(request, ladder_id, match_id):
    ladder = get_object_or_404(Ladder, pk=ladder_id)
    match = get_object_or_404(Match, pk=match_id)
    return render_to_response('leaderboard/match.html',
        {'ladder': ladder, 'match': match},
        context_instance=RequestContext(request)
    )
    
@login_required(login_url="/accounts/login")
def create_match(request, ladder_id):
    ladder = get_ladder_or_404(pk=ladder_id)
    if request.POST:
        form = MatchCreationForm(request.POST)
        if form.is_valid():
            match = form.save(commit=True)
            form = MatchCreationForm()
            form.success = "Match was created successfully"
            logic.adjust_rankings(match)
            if request.is_ajax():
                return render(request, 'leaderboard/match_entry_form.html', {'form': form, 'ladder': ladder})
            return redirect('ladders/{}'.format(ladder_id))
    else:
        form = MatchCreationForm()
    return render(request, 'leaderboard/match_entry_form.html', {'form': form, 'ladder': ladder})

def ajax_ladder_display(request, ladder):
    return render(request, 'leaderboard/ladder_display.html', {'ladder': ladder})

def ajax_match_feed(request, ladder_id):
    match_feed = logic.get_match_feed(get_ladder_or_404(pk=ladder_id))
    return render(request, 'leaderboard/match_feed.html', {'match_feed': match_feed})
