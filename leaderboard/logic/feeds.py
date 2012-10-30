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
