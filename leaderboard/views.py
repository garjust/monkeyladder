from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

from accounts.decorators import login_required_forbidden
from core.logic import get_ladder_or_404
from core.forms import LadderEditForm

from leaderboard.forms import MatchCreationForm, AdvancedMatchCreationForm
from leaderboard import logic
from leaderboard.models import Match
from core.models import Watcher

def view_ladder(request, ladder_id, form=None):
    ladder = get_ladder_or_404(pk=ladder_id)
    games = request.GET.get('games', None)
    if not form:
        form = MatchCreationForm(ladder_id)
    if games:
        form = AdvancedMatchCreationForm(int(games), ladder_id)
    admin = get_admin(request.user, ladder)
    return render(request, 'leaderboard/view_ladder.html', {
        'navbar_active': 'ladder',
        'ladder': ladder,
        'player_names': logic.get_autocomplete_list(ladder),
        'match_feed': logic.get_match_feed(ladder),
        'form': form,
        'admin': admin,
        'not_watching': is_watching(request.user, ladder),
    })

def is_watching(user, ladder):
    if user.is_authenticated():
        try:
            w = ladder.watcher(user)
            return False
        except Watcher.DoesNotExist:
            pass
    return True

def get_admin(user, ladder):
    if user.is_authenticated():
        try:
            return ladder.watcher(user).admin()
        except Watcher.DoesNotExist:
            return False

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

def view_matches(request, ladder_id):
    ladder = get_ladder_or_404(pk=ladder_id)
    paginator = Paginator(ladder.match_set.order_by('-created'), 10)
    page_number = request.GET.get('page')
    try:
        matches = paginator.page(page_number)
    except PageNotAnInteger:
        matches = paginator.page(1)
    except EmptyPage:
        matches = paginator.page(paginator.num_pages)
    match_id = request.GET.get('id', None)
    if match_id:
        match = get_object_or_404(Match, pk=match_id)
        for page_number in range(1, paginator.num_pages + 1):
            page = paginator.page(page_number)
            if match in page:
                matches = page
    return render(request, 'leaderboard/view_matches.html',
        {'navbar_active': 'matches', 'ladder': ladder, 'matches': matches, 'match_id': match_id}
    )

@login_required_forbidden
def create_match(request, ladder_id):
    ladder = get_ladder_or_404(pk=ladder_id)
    if request.POST:
        if request.GET.get('games', None):
            form = AdvancedMatchCreationForm(int(request.GET.get('games')), ladder_id, request.POST)
        else:
            form = MatchCreationForm(ladder_id, request.POST)
        if form.is_valid():
            match = form.save(commit=True)
            logic.adjust_rankings(match)
            if request.is_ajax():
                if request.GET.get('games', None):
                    form = AdvancedMatchCreationForm(int(request.GET.get('games')), ladder_id)
                else:
                    form = MatchCreationForm(ladder_id)
                return render(request, 'leaderboard/content/match_entry_form.html', {'form': form, 'ladder': ladder, 'new_match': match})
            return redirect('/ladders/{}'.format(ladder_id))
    else:
        form = MatchCreationForm(ladder_id)
    return render(request, 'leaderboard/content/match_entry_form.html', {'form': form, 'ladder': ladder})

def ajax_ladder_display(request, ladder_id):
    ladder = get_ladder_or_404(pk=ladder_id)
    return render(request, 'leaderboard/content/ladder_display.html', {'ladder': ladder})

def match_feed_content(request, ladder_id):
    ladder = get_ladder_or_404(pk=ladder_id)
    match_feed = logic.get_match_feed(ladder)
    return render(request, 'leaderboard/content/match_feed.html', {'match_feed': match_feed, 'ladder': ladder})

@login_required
def watch_ladder(request, ladder_id):
    ladder = get_ladder_or_404(pk=ladder_id)
    Watcher.objects.create(ladder=ladder, user=request.user)
    return render(request, 'leaderboard/content/ladder_display.html', {'ladder': ladder})
