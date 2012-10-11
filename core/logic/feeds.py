from core.models import Ladder

import logging
logger = logging.getLogger('monkeyladder')

def public_ladder_feed(user=None, order='-created', size=25):
    """
    Returns a ladder feed with only public ladders

    If a user is supplied, any ladders watched by the user are excluded
    """
    ladders = Ladder.objects.filter(is_private=False).order_by(order)[:size]
    if user and user.is_authenticated:
        watched = watched_ladder_feed(user)
        ladders = filter(lambda l: l not in watched, ladders)
    return ladders

def watched_ladder_feed(user, order='-created', size=25, include_watchers=False, **filters):
    """
    Returns a ladder feed of the users watched ladders

    Optionally also returns the watcher object for each ladder
    """
    if user.is_authenticated():
        watchers = user.watcher_set.filter(**filters).order_by(order)[:size]
        if include_watchers:
            return [(watcher.ladder, watcher) for watcher in watchers]
        return [watcher.ladder for watcher in watchers]
    return []

def nonfavorite_ladder_feed(user, order='-created', size=25, include_watchers=False):
    """
    Returns a ladder feed of the users watched ladders which are not favorites
    """
    return watched_ladder_feed(user, order=order, size=size, include_watchers=include_watchers, favorite=False)

def favorite_ladder_feed(user, order='-created', size=25, include_watchers=False):
    """
    Returns a ladder feed of the users favorite watched ladders
    """
    return watched_ladder_feed(user, order=order, size=size, include_watchers=include_watchers, favorite=True)
