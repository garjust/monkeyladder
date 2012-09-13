from leaderboard.models import Match, MatchPlayer

import logging
logger = logging.getLogger('monkeyladder')

def get_match_feed(ladder=None, order='-created', size=10):
    """
    Returns a match feed for the specified ladder
    """
    query = Match.objects.all()
    if ladder:
        query = query.filter(ladder=ladder)
    return query.order_by(order)[:size]

def get_players_match_feed(user, ladder=None, order='-match__created', size=10):
    """
    Returns a match feed for the specified ladder and user
    """
    query = MatchPlayer.objects.filter(user=user)
    if ladder:
        query = query.filter(match__ladder=ladder)
    return map(lambda p: p.match, query.order_by(order)[:size])

def climbing_ladder_feed(user, order='-created', size=5):
    """
    Returns a ladder feed of the ladders the user is a player on
    """
    if user.is_authenticated():
        return map(lambda p: p.ladder, user.player_set.all().order_by(order)[:size])

