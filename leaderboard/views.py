from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from accounts.decorators import login_required_forbidden
from core.logic import get_ladder_or_404, int_or_404, get_base_ladder_context

from leaderboard.forms import MatchCreationForm, AdvancedMatchCreationForm
from leaderboard import logic
from leaderboard.models import Match

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
    context = get_base_ladder_context(request, ladder)
    context.update({'navbar_active': 'matches', 'ladder': ladder, 'matches': matches, 'match_id': match_id})
    return render(request, 'leaderboard/view_matches.html', context)

@login_required_forbidden
def create_match(request, ladder_id):
    ladder = get_ladder_or_404(pk=ladder_id)
    if request.POST:
        if request.GET.get('games', None):
            form = AdvancedMatchCreationForm(request.GET.get('games'), ladder, request.POST)
        else:
            form = MatchCreationForm(ladder, request.POST)
        if form.is_valid():
            match = form.save(commit=True)
            logic.adjust_rankings(match)
            if request.is_ajax():
                if request.GET.get('games', None):
                    form = AdvancedMatchCreationForm(request.GET.get('games'), ladder)
                else:
                    form = MatchCreationForm(ladder)
                return render(request, 'leaderboard/content/match_entry_form.html', {
                    'player_names': logic.get_ladder_players_for_match_entry(ladder),
                    'form': form,
                    'ladder': ladder,
                    'new_match': match,
                })
            return redirect('/ladders/{}'.format(ladder_id))
    else:
        form = MatchCreationForm(ladder_id)
    return render(request, 'leaderboard/content/match_entry_form.html', {
        'player_names': logic.get_ladder_players_for_match_entry(ladder),
        'form': form,
        'ladder': ladder,
    })

def match_feed_content(request, ladder_id):
    ladder = get_ladder_or_404(pk=ladder_id)
    match_feed = logic.get_match_feed(ladder)
    return render(request, 'leaderboard/content/match_feed.html', {'match_feed': match_feed, 'ladder': ladder})
