from core.models import Ladder

import logging
logger = logging.getLogger('monkeyladder')
        
def has_ladder_permission(user, ladder):
    """
    Determines if a user has permission to view a ladder
    """
    return not ladder.is_private or (user.is_authenticated() and (len(ladder.watcher_set.filter(user=user)) != 0))
    
def public_ladder_feed(order='-created', size=5):
    """
    Returns a ladder feed with only public ladders
    """
    return Ladder.objects.filter(is_private=False).order_by(order)[:size]

def watched_ladder_feed(user, order='-created', size=5):
    """
    Returns a ladder feed of the users watched ladders
    """
    if user.is_authenticated():
        return map(lambda w: w.ladder, user.watcher_set.all().order_by(order)[:size])

def favorite_ladder_feed(user, order='-created', size=25):
    """
    Returns a ladder feed of the users favorite ladders
    """
    if user.is_authenticated():
        return map(lambda f: f.ladder, user.favorite_set.all().order_by(order)[:size])