from core.models import Ladder, Watcher
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404

import logging
logger = logging.getLogger('monkeyladder')


def int_or_404(value):
    """
    Returns the given value cast as an integer or 404 if unsuccessful
    """
    try:
        return int(value)
    except (TypeError, ValueError):
        logger.debug("Failed to cast %s to integer, raising 404" % value)
        raise Http404


def int_or_none(value):
    """
    Returns the given value cast as an integer or None if unsuccessful
    """
    try:
        return int(value)
    except (TypeError, ValueError):
        logger.debug("Failed to cast %s to integer, returning None" % value)
        return None


def empty_string_if_none(value):
    """
    Returns an empty string if value is equal to None
    """
    return '' if value == None else value


def get_ladder_or_404(*args, **kwargs):
    """
    Returns a ladder or a 404 response
    """
    return get_object_or_404(Ladder, *args, **kwargs)


def get_watcher(user, ladder, watcher_type=None):
    """
    If a valid user exists for the user and ladder combination it is returned

    If a watcher type is specified then the watcher type must match to be returned
    """
    if user.is_anonymous():
        return None
    try:
        watcher = user.watcher_set.get(ladder=ladder)
        if watcher_type:
            return watcher if watcher.type == watcher_type else None
        return watcher
    except Watcher.DoesNotExist:
        return None
