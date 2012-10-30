from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from accounts.decorators import login_required_forbidden
from core.decorators import can_view_ladder, login_required_and_ladder_admin, ladder_is_active
from core.logic.util import get_ladder_or_404, int_or_404, get_user_or_404
from core.generic_views import handle_form_and_redirect_to_ladder, view_with_ladder

from leaderboard.forms import get_match_form, LeaderboardConfigurationForm, LadderRankingAndPlayerEditForm
from leaderboard.generic_views import view_with_leaderboard
from leaderboard import logic
from leaderboard.models import Match
from leaderboard.logic.feeds import get_match_feed


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
    return view_with_ladder(request, ladder, 'leaderboard/view_matches.html', {
        'navbar_active': 'matches', 'matches': matches, 'match_id': match_id
    })


@ladder_is_active
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
        else:
            return redirect(ladder)
    return view_with_leaderboard(request, ladder, 'leaderboard/content/match_entry_form.html', form=form)


@ladder_is_active
@can_view_ladder
def view_ladder(request, ladder_id):
    ladder = get_ladder_or_404(pk=ladder_id)
    return view_with_leaderboard(request, ladder, 'leaderboard/view_ladder.html', {'navbar_active': 'ladder'})


@ladder_is_active
@can_view_ladder
def ladder_display(request, ladder_id):
    ladder = get_ladder_or_404(pk=ladder_id)
    return view_with_ladder(request, ladder, 'leaderboard/content/ladder_display.html')


@ladder_is_active
@login_required_and_ladder_admin
def edit_ladder(request, ladder_id):
    return handle_form_and_redirect_to_ladder(request, ladder_id, LadderRankingAndPlayerEditForm, 'leaderboard/content/ladder_display.html',
        form_name='ladder_edit_form'
    )


@ladder_is_active
@login_required_and_ladder_admin
def configure_ladder(request, ladder_id):
    return handle_form_and_redirect_to_ladder(request, ladder_id, LeaderboardConfigurationForm, 'leaderboard/configure_ladder.html',
        context={'navbar_active': 'config'}
    )


@login_required_forbidden
def matchup(request):
    """
    Return a piece of HTML designed to be embedded in the matchup container
    """
    pass


@login_required_forbidden
def matches(request):
    """
    Returns a paged feed of matches
    """
    filters = {}
    if request.GET.get('ladder_id'):
        filters['ladder'] = request.GET.get('ladder_id')
    if request.GET.get('user_id'):
        filters['user'] = request.GET.get('user_id')
    paginator = Paginator(get_match_feed(**filters), 5)
    page_number = request.GET.get('page')
    try:
        matches = paginator.page(page_number)
    except PageNotAnInteger:
        matches = paginator.page(1)
    except EmptyPage:
        matches = paginator.page(paginator.num_pages)
    context = {'match_feed': matches}
    if filters.get('ladder'):
        context['matches_ladder'] = get_ladder_or_404(pk=filters['ladder'])
    if filters.get('user'):
        context['matches_user'] = get_user_or_404(pk=filters['user'])
    return render(request, 'leaderboard/content/match_feed.html', context)
