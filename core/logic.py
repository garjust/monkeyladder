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

def ladder_watchers(ladder, order='-created', size=100):
    """
    Returns a list of watchers for the given ladder
    """
    return ladder.watcher_set.order_by(order)[:size]

def create_watcher(ladder, user, created_by, watcher_type='NORMAL'):
    """
    Creates a watcher object
    """
    return Watcher.objects.create(ladder=ladder, user=user, type=watcher_type, created_by=created_by)

def get_watcher(user, ladder):
    """
    Retrieves the watcher object associated with user and ladder or None if it does not exist
    """
    if user.is_authenticated():
        try:
            return ladder.watcher(user)
        except Watcher.DoesNotExist:
            pass

def _get_single_config(ladder, key):
    config_key = LadderConfigurationKey.objects.get(key=key)
    try:
        config = LadderConfiguration.objects.get(ladder=ladder, key=config_key)
    except LadderConfiguration.DoesNotExist:
        config = LadderConfiguration.objects.get(ladder=None, key=config_key)
    return config.value()

def _put_single_config(ladder, key, dictionary=None):
    """
    Retrieves the value of the configuration key for the given ladder

    If the ladder specified does not have a configration for the key the default is used
    """
    if not dictionary:
        dictionary = {}
    dictionary[key] = _get_single_config(ladder, key)
    return dictionary

def get_config(ladder, key, *keys):
#    config = {key: _get_single_config(ladder, key)}
#    for key in keys:
#        config[key] = _get_single_config(ladder, key)
    config = reduce(lambda dictionary, key: _put_single_config(ladder, key, dictionary), keys, _put_single_config(ladder, key))
    return config[key] if len(config) == 1 else config
