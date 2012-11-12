from django.contrib.auth.models import User
from django.db.models import Q
from leaderboard.models import Ladder, Match

import logging
logger = logging.getLogger('monkeyladder')


def get_match_feed(ladder=None, user=None, order='-created'):
    """
    Returns a match feed

    The matches can be specific to a ladder and/or a user
    """
    query = Match.objects.all()
    if user:
        query = query.filter(matchplayer__user=user)
    if ladder:
        query = query.filter(ladder=ladder)
    return query.order_by(order)


def get_played_ladder_feed(user, climbing=True, has_matches=True, order='-created'):
    """
    Returns a ladder feed of all the ladders the user is playing on or has matches on
    """
    if user.is_authenticated():
        climbing_filter = Q(ranked__player__user=user)
        has_matches_filter = Q(match__matchplayer__user=user)
        if climbing and has_matches:
            query = Ladder.objects.filter(climbing_filter | has_matches_filter)
        else:
            query = Ladder.objects.filter(climbing_filter if climbing else has_matches_filter)
        return query.distinct().order_by(order)


def users_played(user_id, ladder_id=None):
    """
    Returns a list of users who have played in a match with the given user
    """
    filters = {'matchplayer__match__matchplayer__user': user_id}
    if ladder_id:
        filters['matchplayer__match__ladder'] = ladder_id
    return User.objects.filter(**filters).distinct().exclude(pk=user_id)
