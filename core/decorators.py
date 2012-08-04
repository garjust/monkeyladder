from django.http import HttpResponseForbidden

from core.models import Watcher

def can_view_ladder(f):
    pass

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
