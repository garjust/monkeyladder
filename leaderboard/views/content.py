from accounts.decorators import login_required_forbidden
from core.decorators import can_view_ladder, login_required_and_ladder_admin, ladder_is_active
from core.generic_views import view_with_ladder, handle_form
from core.logic.util import get_ladder_or_404, get_user_or_404, get_page_or_first_page, get_page_with_object_id, int_or_none, empty_string_if_none
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render
from django.views.generic.list_detail import object_detail
from leaderboard.decorators import ladder_player_or_admin
from leaderboard.forms import get_match_form, LadderRankingAndPlayerEditForm
from leaderboard.logic.feeds import get_match_feed, users_played, get_played_ladder_feed
from leaderboard.logic.rankings import adjust_rankings
from leaderboard.logic.stats import get_stats
from leaderboard.models import Match


@ladder_is_active
@ladder_player_or_admin
def create_match(request, ladder_id):
    ladder = get_ladder_or_404(pk=ladder_id)
    games = request.GET.get('games')
    if request.POST:
        form = get_match_form(ladder, post_dictionary=request.POST, number_of_games=games)
        if form.is_valid():
            match = form.save()
            adjust_rankings(match)
            form = get_match_form(ladder, number_of_games=games)
            form.success = "Match created successfully"
    else:
        form = get_match_form(ladder, number_of_games=games)
    return view_with_ladder(request, ladder, 'leaderboard/content/match_entry_form.html', context={'form': form})


@ladder_is_active
@can_view_ladder
def display_ladder(request, ladder_id):
    ladder = get_ladder_or_404(pk=ladder_id)
    return view_with_ladder(request, ladder, 'leaderboard/content/ladder_display.html')


@ladder_is_active
@login_required_and_ladder_admin
def edit_ladder(request, ladder_id):
    form_result = handle_form(request, ladder_id, LadderRankingAndPlayerEditForm, 'leaderboard/content/edit_ladder.html',
        form_name='ladder_edit_form',
    )
    return form_result if not request.POST else display_ladder(request, ladder_id)


@login_required_forbidden
def matchups(request):
    """
    Return a piece of HTML designed to be embedded in the matchup container
    """
    ladder_id = empty_string_if_none(int_or_none(request.GET.get('ladder_id')))
    user_id = empty_string_if_none(int_or_none(request.GET.get('user_id')))
    page_number = empty_string_if_none(int_or_none(request.GET.get('page')))
    size = empty_string_if_none(int_or_none(request.GET.get('size', 5)))

    if ladder_id:
        ladder = get_ladder_or_404(pk=ladder_id)
    if user_id:
        user = get_user_or_404(pk=user_id)

    context = {
        'matchup_user': user if user_id else user_id,
        'feed_ladder': ladder if ladder_id else ladder_id,
        'feed_ladder_options': get_played_ladder_feed(user, order='name') if user_id else None,
    }

    paginator = Paginator(users_played(user_id=user_id, ladder_id=ladder_id), size)
    matchup_users = get_page_or_first_page(paginator, page_number)

    matchups = []
    for matchup_user in matchup_users:
        matchup = get_stats(user_id, ladder=ladder_id, other_user_id=matchup_user.id)
        matchup['user'] = matchup_user
        if ladder_id:
            matchup['ladder_id'] = ladder_id
        matchups.append(matchup)
    context['feed'] = matchup_users
    context['feed_data'] = matchups

    context['feed_info'] = {
        'name': 'Matchups',
        'prefix': 'matchup',
        'span_name': 'matchup-feed-span',
        'span_size': 6,
        'url': '/ladders/leaderboard/content/matchups/',
        'url_parameters': {
            'ladder_id': ladder_id if ladder_id else '',
            'user_id': user_id if user_id else '',
            'size': size,
        },
    }
    return render(request, 'leaderboard/content/matchup_feed.html', context)


def matches(request):
    """
    Returns a paged feed of matches
    """
    ladder_id = empty_string_if_none(int_or_none(request.GET.get('ladder_id')))
    match_id = empty_string_if_none(int_or_none(request.GET.get('match_id')))
    user_id = empty_string_if_none(int_or_none(request.GET.get('user_id')))
    page_number = empty_string_if_none(int_or_none(request.GET.get('page')))
    size = empty_string_if_none(int_or_none(request.GET.get('size', 5)))

    if ladder_id:
        ladder = get_ladder_or_404(pk=ladder_id)
    if user_id:
        user = get_user_or_404(pk=user_id)

    paginator = Paginator(get_match_feed(ladder=ladder_id, user=user_id), size)
    if match_id:
        matches = get_page_with_object_id(paginator, match_id)
    else:
        matches = get_page_or_first_page(paginator, page_number)

    context = {'feed': matches, 'match_feed_size': size,
        'match_id': match_id,
        'feed_ladder': ladder if ladder_id else ladder_id,
        'matches_user': user if user_id else user_id,
        'feed_ladder_options': get_played_ladder_feed(user, order='name') if user_id else None,
    }

    context['feed_info'] = {
        'name': 'Match History',
        'prefix': 'match',
        'span_name': 'match-feed-span',
        'span_size': 6,
        'url': '/ladders/leaderboard/content/matches/',
        'url_parameters': {
            'ladder_id': ladder_id if ladder_id else '',
            'user_id': user_id if user_id else '',
            'size': size,
        },
    }
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
    if ladder_id:
        context['stats_ladder'] = get_ladder_or_404(pk=ladder_id)
    context['stats_user_ladders'] = get_played_ladder_feed(context['stats_user'], order='name')
    context['stats'] = get_stats(user_id, ladder=ladder_id)
    return render(request, 'leaderboard/content/player_stats.html', context)


def match(request, match_id):
    return object_detail(request, Match.objects.filter(pk=match_id), match_id, template_name='leaderboard/content/match.html', template_object_name='match')
