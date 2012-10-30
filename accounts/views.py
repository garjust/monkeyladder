from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from accounts import logic
from accounts.forms import ExtendedUserCreationForm
from core.logic.feeds import watched_ladder_feed


def register(request):
    if request.POST:
        form = ExtendedUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/accounts/login")
    else:
        form = ExtendedUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required(login_url="/accounts/login")
def view_profile(request, user_id):
    user = logic.get_user_or_404(pk=user_id)
    return render(request, 'accounts/view_profile.html', {
        'user': user,
        'watched_feed': watched_ladder_feed(user, include_watchers=True),
    })


@login_required(login_url="/accounts/login")
def edit_profile(request, user_id):
    return render(request, 'accounts/edit_profile.html')
