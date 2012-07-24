from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

from accounts.decorators import login_required_forbidden
from core.logic import get_ladder_or_404, int_or_404
from core.forms import LadderEditForm

from leaderboard.forms import MatchCreationForm, AdvancedMatchCreationForm
from leaderboard import logic
from leaderboard.models import Match

def view_ladder(request, ladder_id, context={}, form=None):
    ladder = get_ladder_or_404(pk=ladder_id)
    games = request.GET.get('games', None)
    if not form:
        form = MatchCreationForm(ladder_id)
    if games:
        form = AdvancedMatchCreationForm(games, ladder_id)
    context.update({
        'player_names': logic.get_autocomplete_list(ladder),
        'match_feed': logic.get_match_feed(ladder),
        'form': form,
    })
    return render(request, 'leaderboard/view_ladder.html', context)

def edit_ladder(request, ladder_id):
    ladder = get_ladder_or_404(pk=ladder_id)
    if request.POST:
        form = LadderEditForm(ladder, request.POST)
        if form.is_valid():
            form.save(ladder)
            return redirect(ladder)
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
        match_id = int_or_404(match_id)
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
            form = AdvancedMatchCreationForm(request.GET.get('games'), ladder_id, request.POST)
        else:
            form = MatchCreationForm(ladder_id, request.POST)
        if form.is_valid():
            match = form.save(commit=True)
            logic.adjust_rankings(match)
            if request.is_ajax():
                if request.GET.get('games', None):
                    form = AdvancedMatchCreationForm(request.GET.get('games'), ladder_id)
                else:
                    form = MatchCreationForm(ladder_id)
                return render(request, 'leaderboard/content/match_entry_form.html', {'form': form, 'ladder': ladder, 'new_match': match})
            return redirect('/ladders/{}'.format(ladder_id))
    else:
        form = MatchCreationForm(ladder_id)
    return render(request, 'leaderboard/content/match_entry_form.html', {'form': form, 'ladder': ladder})

def ladder_display_content(request, ladder_id):
    ladder = get_ladder_or_404(pk=ladder_id)
    return render(request, 'leaderboard/content/ladder_display.html', {'ladder': ladder})

def match_feed_content(request, ladder_id):
    ladder = get_ladder_or_404(pk=ladder_id)
    match_feed = logic.get_match_feed(ladder)
    return render(request, 'leaderboard/content/match_feed.html', {'match_feed': match_feed, 'ladder': ladder})
