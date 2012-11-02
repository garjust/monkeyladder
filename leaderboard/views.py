from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.list_detail import object_detail

from accounts.decorators import login_required_forbidden
from core.decorators import can_view_ladder, login_required_and_ladder_admin, ladder_is_active
from core.logic.util import get_ladder_or_404, get_user_or_404
from core.generic_views import handle_form_and_redirect_to_ladder, view_with_ladder

from leaderboard.forms import get_match_form, LeaderboardConfigurationForm, LadderRankingAndPlayerEditForm
from leaderboard.generic_views import view_with_leaderboard
from leaderboard import logic
from leaderboard.models import Match
from leaderboard.logic.feeds import get_match_feed, climbing_ladder_feed, users_played
from leaderboard.logic.stats import calculate_players_game_win_percentage, calculate_players_match_win_percentage, get_stats


@can_view_ladder
def matches_page(request, ladder_id):
    ladder = get_ladder_or_404(pk=ladder_id)
    match_id = request.GET.get('id', None)
    return view_with_ladder(request, ladder, 'leaderboard/matches_page.html', {
        'navbar_active': 'matches', 'match_id': match_id, 'match_feed_size': 10,
    })


@ladder_is_active
@login_required_forbidden
@can_view_ladder
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
def ladder_page(request, ladder_id):
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
    ladder_id = request.GET.get('ladder_id')
    user_id = request.GET.get('user_id')
    page_number = request.GET.get('page_number')
    size = request.GET.get('size')
    if not size:
        size = 5
    context = {'matchups_size': size}
    paginator = Paginator(users_played(user_id=user_id, ladder_id=ladder_id), size)
    try:
        matchup_users = paginator.page(page_number)
    except PageNotAnInteger:
        matchup_users = paginator.page(1)
    except EmptyPage:
        matchup_users = paginator.page(paginator.num_pages)
    context['matchup_users'] = matchup_users
    matchups = []
    for matchup_user in matchup_users:
        matchup = get_stats(user_id, ladder=ladder_id, other_user_id=matchup_user.id)
        matchup['user'] = matchup_user
        if ladder_id:
            matchup['ladder_id'] = ladder_id
        matchups.append(matchup)
    context['matchups'] = matchups
    return render(request, 'leaderboard/content/matchups.html', context)


def matches(request):
    """
    Returns a paged feed of matches
    """
    ladder_id = request.GET.get('ladder_id')
    user_id = request.GET.get('user_id')
    page_number = request.GET.get('page')
    size = request.GET.get('size')
    if not size:
        size = 5
    filters = {}
    if ladder_id and ladder_id != "0":
        filters['ladder'] = ladder_id
    if user_id:
        filters['user'] = user_id
    paginator = Paginator(get_match_feed(**filters), size)
    try:
        matches = paginator.page(page_number)
    except PageNotAnInteger:
        matches = paginator.page(1)
    except EmptyPage:
        matches = paginator.page(paginator.num_pages)
    context = {'match_feed': matches, 'match_feed_size': size}
    if filters.get('ladder'):
        context['matches_ladder'] = get_ladder_or_404(pk=filters['ladder'])
    if filters.get('user'):
        context['matches_user'] = get_user_or_404(pk=filters['user'])
        context['matches_user_ladders'] = climbing_ladder_feed(context['matches_user'])
    if request.GET.get('match_bucket'):
        context['match_bucket'] = True
    return render(request, 'leaderboard/content/match_feed.html', context)


@login_required_forbidden
def stats(request):
    """
    Returns statistics for the given user
    """
    user_id = request.GET.get('user_id')
    ladder_id = request.GET.get('ladder_id')
    if not user_id:
        raise Http404()
    context = {'stats_user': get_user_or_404(pk=user_id), 'stats_ladder': None}
    if ladder_id and ladder_id != "0":
        print "HERE"
        context['stats_ladder'] = get_ladder_or_404(pk=ladder_id)
    context['stats_user_ladders'] = climbing_ladder_feed(context['stats_user'])
    context.update({
        'match_win_percentage': calculate_players_match_win_percentage(context['stats_user'], ladder=context['stats_ladder']),
        'game_win_percentage': calculate_players_game_win_percentage(context['stats_user'], ladder=context['stats_ladder']),
    })
    return render(request, 'leaderboard/content/player_stats.html', context)


def match(request, match_id):
    return object_detail(request, Match.objects.filter(pk=match_id), match_id, template_name='leaderboard/content/match.html', template_object_name='match')
