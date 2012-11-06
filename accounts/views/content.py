from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render

import logging
logger = logging.getLogger('monkeyladder')


def user_info(request, user_id):
    return render(request, 'accounts/content/user_info.html')


@login_required(login_url="/accounts/login")
def edit_user_info(request, user_id):
    if request.user.id == user_id:
        return render(request, 'accounts/content/edit_user_info.html')
    return HttpResponseForbidden()
