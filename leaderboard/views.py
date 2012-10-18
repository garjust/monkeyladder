from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from accounts.decorators import login_required_forbidden
from core.decorators import can_view_ladder, login_required_and_ladder_admin
from core.logic.util import get_ladder_or_404, int_or_404, get_base_ladder_context, get_watcher
from core.generic_views import handle_form_and_redirect_to_ladder

from leaderboard.contexts import get_leaderboard_ladder_context, view_ladder_context, ladder_display_context
from leaderboard.forms import get_match_form, LeaderboardConfigurationForm, LadderRankingAndPlayerEditForm
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
    context.update({'navbar_active': 'matches', 'matches': matches, 'match_id': match_id})
    return render(request, 'leaderboard/view_matches.html', context)

@login_required_forbidden
def create_match(request, ladder_id):
    ladder = get_ladder_or_404(pk=ladder_id)
    form = get_match_form(ladder, post_dictionary=request.POST, number_of_games=request.GET.get('games'))
    if form.is_valid():
        match = form.save()
        logic.rankings.adjust_rankings(match)
        if request.is_ajax():
            form = get_match_form(ladder, number_of_games=request.GET.get('games'))
            form.success = "Match created successfully"
            return render(request, 'leaderboard/content/match_entry_form.html', get_leaderboard_ladder_context(request, ladder, form=form))
        return redirect('/ladders/{}'.format(ladder_id))
    return render(request, 'leaderboard/content/match_entry_form.html', get_leaderboard_ladder_context(request, ladder, form=form))

def match_feed_content(request, ladder_id):
    ladder = get_ladder_or_404(pk=ladder_id)
    match_feed = logic.feeds.get_match_feed(ladder)
    return render(request, 'leaderboard/content/match_feed.html', {'match_feed': match_feed, 'ladder': ladder})

@can_view_ladder
def view_ladder(request, ladder_id):
    ladder = get_ladder_or_404(pk=ladder_id)
    context = get_base_ladder_context(request, ladder, extra={'navbar_active': 'ladder'})
    context.update(view_ladder_context(request, ladder))
    return render(request, 'leaderboard/view_ladder.html', context)

@can_view_ladder
def ladder_display(request, ladder_id, context=None):
    if not context:
        context = {}
    ladder = get_ladder_or_404(pk=ladder_id)
    context = get_base_ladder_context(request, ladder, extra=context)
    context.update(ladder_display_context(request, ladder))
    return render(request, 'leaderboard/content/ladder_display.html', context)

@login_required_and_ladder_admin
def edit_ladder(request, ladder_id):
    return handle_form_and_redirect_to_ladder(request, ladder_id, LadderRankingAndPlayerEditForm, 'leaderboard/content/ladder_display.html',
        form_name='ladder_edit_form'
    )

@login_required_and_ladder_admin
def configure_ladder(request, ladder_id):
    return handle_form_and_redirect_to_ladder(request, ladder_id, LeaderboardConfigurationForm, 'leaderboard/configure_ladder.html',
        extra_context={'navbar_active': 'config'}
    )
