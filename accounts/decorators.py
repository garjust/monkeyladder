from django.http import HttpResponseForbidden

def login_required_forbidden(f):
    """
    A simple check to see if a user is logged in just like login_required BUT returns a 403 instead of redirecting
    """
    def decorated(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseForbidden()
        else:
            return f(request, *args, **kwargs)
    return decorated
        