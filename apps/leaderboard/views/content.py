from accounts.decorators import login_required_forbidden
from accounts.logic import get_user_or_404
from django.core.paginator import Paginator
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.views.generic.list_detail import object_detail
from ladders.decorators import can_view_ladder
from ladders.decorators import ladder_is_active
from ladders.decorators import login_required_and_ladder_admin
from ladders.generic_views import handle_form
from ladders.generic_views import view_with_ladder
from ladders.logic.pagination import get_page
from ladders.logic.pagination import get_page_with_item
from ladders.logic.util import empty_string_if_none
from ladders.logic.util import get_ladder_or_404
from ladders.logic.util import int_or_none
from leaderboard.decorators import ladder_player_or_admin
from leaderboard.forms import LadderRankingAndPlayerEditForm
from leaderboard.forms import get_match_form
from leaderboard.logic.feeds import get_match_feed
from leaderboard.logic.feeds import get_played_ladder_feed
from leaderboard.logic.feeds import users_played
from leaderboard.logic.rankings import adjust_rankings
from leaderboard.logic.rankings import get_ladder_players_for_match_entry
from leaderboard.logic.stats import get_stats
from leaderboard.models import Match


@ladder_is_active
@ladder_player_or_admin
def create_match(request, ladder_id):
    ladder = get_ladder_or_404(pk=ladder_id)
    games = int_or_none(request.GET.get('games'))
    if request.POST:
        form = get_match_form(ladder, post_dictionary=request.POST, number_of_games=games)
        if form.is_valid():
            match = form.save()
            adjust_rankings(match)
            form = get_match_form(ladder, number_of_games=games)
            form.success = "Match created successfully"
    else:
        form = get_match_form(ladder, number_of_games=games)
    return view_with_ladder(request, ladder, 'leaderboard/content/match_entry_form.html',
        context={'form': form, 'ladder_players': get_ladder_players_for_match_entry(ladder)}
    )


@ladder_is_active
@can_view_ladder
def display_ladder(request, ladder_id):
    ladder = get_ladder_or_404(pk=ladder_id)
    return view_with_ladder(request, ladder, 'leaderboard/content/ladder.html')


@ladder_is_active
@login_required_and_ladder_admin
def edit_ladder(request, ladder_id):
    form_result = handle_form(request, ladder_id, LadderRankingAndPlayerEditForm, 'leaderboard/content/edit_ladder.html',
        form_name='ladder_edit_form',
    )
    return form_result if not request.POST else display_ladder(request, ladder_id)


@login_required_forbidden
def matchups(request):
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
    page = get_page(paginator, page_number)
    context['feed'] = page

    for matchup_user in page:
        matchup_user.stats = get_stats(user_id, ladder=ladder_id, other_user_id=matchup_user.id)
        matchup_user.user = matchup_user
        if ladder_id:
            matchup_user.ladder = ladder

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
    page = get_page_with_item(paginator, match_id) if match_id else get_page(paginator, page_number)

    context = {'feed': page, 'match_feed_size': size,
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


def match(request, match_id):
    return object_detail(request, Match.objects.filter(pk=match_id), match_id,
        template_name='leaderboard/content/match.html',
        template_object_name='match'
    )


@login_required_forbidden
def stats(request):
    """
    Returns statistics for the given user
    """
    user_id = empty_string_if_none(int_or_none(request.GET.get('user_id')))
    ladder_id = empty_string_if_none(int_or_none(request.GET.get('ladder_id')))
    if not user_id:
        return HttpResponseBadRequest()
    context = {'stats_user': get_user_or_404(pk=user_id), 'stats_ladder': None}
    if ladder_id:
        context['stats_ladder'] = get_ladder_or_404(pk=ladder_id)
    context['stats_user_ladders'] = get_played_ladder_feed(context['stats_user'], order='name')
    context['stats'] = get_stats(user_id, ladder=ladder_id)
    return render(request, 'leaderboard/content/player_stats.html', context)
