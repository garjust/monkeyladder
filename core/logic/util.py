from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import Http404

from core.models import Ladder

import logging
logger = logging.getLogger('monkeyladder')


def int_or_404(value):
    """
    Returns the given value cast as an integer or 404 if unsuccessful
    """
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


def get_user_or_404(*args, **kwargs):
    """
    Returns a user or a 404 response
    """
    return get_object_or_404(User, *args, **kwargs)
