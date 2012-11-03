from django.contrib.auth.models import User
from django.core.paginator import InvalidPage
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
        return int(value)
    except (TypeError, ValueError):
        raise Http404


def int_or_none(value):
    """
    Returns the given value cast as an integer or None if unsuccessful
    """
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


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


def get_page_or_first_page(paginator, page_number):
    """
    Returns the requested page from the paginator

    If any errors occur the first page is returned
    """
    try:
        return paginator.page(page_number)
    except InvalidPage:
        return paginator.page(1)


def get_page_with_object_id(paginator, object_id):
    for page_number in range(1, paginator.num_pages + 1, 1):
        page = paginator.page(page_number)
        if int(object_id) in [item.pk for item in page]:
            return page
    return paginator.page(1)
