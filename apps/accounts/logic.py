from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


def get_user_or_404(*args, **kwargs):
    """
    Returns a user or a 404 response
    """
    return get_object_or_404(User, *args, **kwargs)
