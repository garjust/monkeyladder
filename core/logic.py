from django.shortcuts import get_object_or_404
from django.http import Http404

from core.models import Ladder, Watcher, LadderConfiguration, LadderConfigurationKey

import logging
logger = logging.getLogger('monkeyladder')

def int_or_404(value):
    try:
        value = int(value)
    except ValueError:
        raise Http404
    return value

def get_base_ladder_context(request, ladder, extra={}):
    """
    Returns the basic context all ladders need
    """
    context = {
        'ladder': ladder,
        'watcher': get_watcher(request.user, ladder)
    }
    context.update(extra)
    return context

def get_ladder_or_404(*args, **kwargs):
    """
    Returns a ladder or a 404 response
    """
    return get_object_or_404(Ladder, *args, **kwargs)

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

def watched_ladder_feed(user, order='-created', size=25, include_watchers=False, filters={}):
    """
    Returns a ladder feed of the users watched ladders

    Optionally also returns the watcher object for each ladder
    """
    if user.is_authenticated():
        watchers = user.watcher_set.filter(**filters).order_by(order)[:size]
        if include_watchers:
            return map(lambda watcher: (watcher.ladder, watcher), watchers)
        return map(lambda watcher: watcher.ladder, watchers)
    return []

def nonfavorite_ladder_feed(user, order='-created', size=25, include_watchers=False):
    """
    Returns a ladder feed of the users watched ladders which are not favorites
    """
    return watched_ladder_feed(user, order=order, size=size, include_watchers=include_watchers, filters={'favorite': False})

def favorite_ladder_feed(user, order='-created', size=25, include_watchers=False):
    """
    Returns a ladder feed of the users favorite watched ladders
    """
    return watched_ladder_feed(user, order=order, size=size, include_watchers=include_watchers, filters={'favorite': True})

def ladder_watchers(ladder, order='-created', size=100):
    """
    Returns a list of watchers for the given ladder
    """
    return ladder.watcher_set.order_by(order)[:size]

def get_watcher(user, ladder):
    """
    Retrieves the watcher object associated with user and ladder or None if it does not exist
    """
    if user.is_authenticated():
        try:
            return ladder.watcher(user)
        except Watcher.DoesNotExist:
            pass

def get_config(ladder, key):
    config_key = LadderConfigurationKey.objects.get(key=key)
    try:
        return LadderConfiguration.objects.get(ladder=ladder, key=config_key).value()
    except LadderConfiguration.DoesNotExist:
        return LadderConfiguration.objects.get(ladder=None, key=config_key).value()
