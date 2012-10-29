from django.http import HttpResponseForbidden, HttpResponseNotFound
from django.shortcuts import redirect

from core.logic.util import get_ladder_or_404
from core.models import Watcher


def ladder_is_active(f):
    """
    Checks whether the ladder specified is active

    If the ladder is not active a 404 response is returned
    """
    def decorated(request, ladder_id, *args, **kwargs):
        ladder = get_ladder_or_404(pk=ladder_id)
        if not ladder.is_active:
            return HttpResponseNotFound()
        return f(request, ladder_id, *args, **kwargs)
    return decorated


def can_view_ladder(f):
    """
    Checks whether the requests user has permission to view the ladder
    """
    def decorated(request, ladder_id, *args, **kwargs):
        ladder = get_ladder_or_404(pk=ladder_id)
        if ladder.is_private and not (request.user.is_authenticated() and (len(ladder.watcher_set.filter(user=request.user)) != 0)):
            return redirect('/home/')
        return f(request, ladder_id, *args, **kwargs)
    return decorated


def login_required_and_ladder_admin(f):
    """
    Requires a logged in user that is watching the ladder and is an admin

    Returns an 403 response
    """
    def decorated(request, ladder_id, *args, **kwargs):
        try:
            if not request.user.is_authenticated() or request.user.watcher_set.get(ladder=ladder_id).type != 'ADMIN':
                raise Watcher.DoesNotExist()
        except Watcher.DoesNotExist:
            return HttpResponseForbidden()
        return f(request, ladder_id, *args, **kwargs)
    return decorated
