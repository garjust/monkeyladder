from accounts import logic
from accounts.forms import ExtendedUserCreationForm
from core.logic.feeds import watched_ladder_feed
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect

import logging
logger = logging.getLogger('monkeyladder')


def register_page(request):
    if request.POST:
        form = ExtendedUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/accounts/login")
    else:
        form = ExtendedUserCreationForm()
    return render(request, 'accounts/register_page.html', {'form': form})


@login_required(login_url="/accounts/login")
def profile_page(request, user_id):
    user = logic.get_user_or_404(pk=user_id)
    return render(request, 'accounts/profile_page.html', {
        'user': user,
        'watched_feed': watched_ladder_feed(user, include_watchers=True),
    })


@login_required(login_url="/accounts/login")
def edit_profile_page(request, user_id):
    if request.user.id == user_id:
        return render(request, 'accounts/edit_profile_page.html')
    return HttpResponseForbidden()
