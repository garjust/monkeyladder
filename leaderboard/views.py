from django.shortcuts import render, redirect

from accounts.decorators import login_required_forbidden
from core.logic import get_ladder_or_404
from core.forms import LadderEditForm

from leaderboard.forms import MatchCreationForm, AdvancedMatchCreationForm
from leaderboard import logic

def view_ladder(request, ladder_id, form=None):
    ladder = get_ladder_or_404(pk=ladder_id)
    games = request.GET.get('games', None)
    if not form:
        form = MatchCreationForm()
    if games:
        form = AdvancedMatchCreationForm(int(games))
    admin = get_admin(request.user, ladder)
    return render(request, 'leaderboard/view_ladder.html', {
        'navbar_active': 'ladder',
        'ladder': ladder,
        'player_names': logic.get_autocomplete_list(ladder),
        'match_feed': logic.get_match_feed(ladder),
        'form': form,
        'games': games,
        'admin': admin,
    })

def get_admin(user, ladder):
    if user.is_authenticated():
        return ladder.watcher(user).admin()

def edit_ladder(request, ladder_id):
    ladder = get_ladder_or_404(pk=ladder_id)
    admin = get_admin(request.user, ladder)
    if request.POST:
        form = LadderEditForm(ladder, request.POST)
        if form.is_valid():
            form.save(ladder)
            return render(request, 'leaderboard/content/ladder_display.html', {'ladder': ladder, 'admin': admin})
        print "FORM INVALID:\n{}".format(form.errors)
    else:
        form = LadderEditForm(ladder)
    return render(request, 'leaderboard/content/ladder_edit.html', {'ladder': ladder, 'ladder_edit_form': form})

def matches(request, ladder_id):
    ladder = get_ladder_or_404(pk=ladder_id)
    matches = ladder.match_set.filter().order_by('-created')
    match_id = request.GET.get('id', None)
    return render(request, 'leaderboard/view_matches.html',
        {'navbar_active': 'matches', 'ladder': ladder, 'matches': matches, 'match_id': match_id}
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
                return render(request, 'leaderboard/content/match_entry_form.html', {'form': form, 'ladder': ladder, 'new_match': match})
            return redirect('ladders/{}'.format(ladder_id))
    else:
        form = MatchCreationForm()
    return render(request, 'leaderboard/content/match_entry_form.html', {'form': form, 'ladder': ladder})

def ajax_ladder_display(request, ladder_id):
    ladder = get_ladder_or_404(pk=ladder_id)
    return render(request, 'leaderboard/content/ladder_display.html', {'ladder': ladder})

def match_feed_content(request, ladder_id):
    match_feed = logic.get_match_feed(get_ladder_or_404(pk=ladder_id))
    return render(request, 'leaderboard/content/match_feed.html', {'match_feed': match_feed})
