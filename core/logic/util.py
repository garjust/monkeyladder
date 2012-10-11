from django.shortcuts import get_object_or_404
from django.http import Http404

from core.models import Ladder, Watcher

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
