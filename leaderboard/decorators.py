from django.http import HttpResponseForbidden


def ladder_player_or_admin(f):
    """
    Checks whether the requests user is a player on the ladder or an admin

    If not a 404 response is returned
    """
    def decorated(request, ladder_id, *args, **kwargs):
        if request.user.is_authenticated() and (request.user.watcher_set.get(ladder=ladder_id).type == 'ADMIN' or request.user.player_set.filter(ladder=ladder_id).count() != 0):
            return f(request, ladder_id, *args, **kwargs)
        return HttpResponseForbidden()
    return decorated