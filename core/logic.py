from django.shortcuts import get_object_or_404

from core.models import Ladder

import logging
logger = logging.getLogger('monkeyladder')

def get_ladder_or_404(*args, **kwargs):
    """
    Returns a ladder or a 404 response
    """
    return get_object_or_404(Ladder, *args, **kwargs)
    
def can_view_ladder(user, ladder):
    """
    Determines if a user has permission to view a ladder
    """
    return not ladder.is_private or (user.is_authenticated() and (len(ladder.watcher_set.filter(user=user)) != 0))
    
def public_ladder_feed(user=None, order='-created', size=5):
    """
    Returns a ladder feed with only public ladders
    
    If a user is supplied, any ladders watched by the user are excluded
    """
    ladders = Ladder.objects.filter(is_private=False).order_by(order)[:size]
    if user and user.is_authenticated:
        watched = watched_ladder_feed(user)
        ladders = filter(lambda l: l not in watched, ladders)
    return ladders

def watched_ladder_feed(user, order='-created', size=25):
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
    
def ladder_watchers(ladder, order='-created', size=100):
    """
    Returns a list of watchers for the given ladder
    """
    return ladder.watcher_set.order_by(order)[:size]