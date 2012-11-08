from django.http import HttpResponseForbidden
from core.logic.util import get_watcher


def ladder_player_or_admin(f):
    """
    Checks whether the requests user is a player on the ladder or an admin

    If not a 404 response is returned
    """
    def decorated(request, ladder_id, *args, **kwargs):
        if request.user.is_authenticated() and (get_watcher(request.user, ladder_id, 'ADMIN') or request.user.player_set.filter(ladder=ladder_id).count() != 0):
            return f(request, ladder_id, *args, **kwargs)
        return HttpResponseForbidden()
    return decorated
