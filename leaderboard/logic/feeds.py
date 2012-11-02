from django.contrib.auth.models import User
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


def climbing_ladder_feed(user, order='-created', size=5):
    """
    Returns a ladder feed of the ladders the user is a player on
    """
    if user.is_authenticated():
        return Ladder.objects.filter(ranked__player__user=user).order_by(order)[:size]


def users_played(user_id, ladder_id=None):
    """
    Returns a list of users who have played in a match with the given user
    """
    filters = {'matchplayer__match__matchplayer__user': user_id}
    if ladder_id:
        filters['matchplayer__match__ladder'] = ladder_id
    return User.objects.filter(**filters).distinct().exclude(pk=user_id)
