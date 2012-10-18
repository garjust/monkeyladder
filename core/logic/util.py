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


def get_lowest_rank(ladder):
    """
    Returns the lowest current rank in the ladder
    """
    return list(ladder.ranking())[-1].rank


def validate_and_correct_ranking(ladder):
    for i, ranked in enumerate(ladder.ranking()):
        if ranked.rank != i + 1:
            ranked.rank = i + 1
            ranked.save()
