from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from accounts import logic
from accounts.forms import ExtendedUserCreationForm
from core.models import Ladder, Watcher
from leaderboard.logic import get_players_match_feed

def register(request):
    if request.POST:
        form = ExtendedUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            form = ExtendedUserCreationForm()
            form.success = True
            return render(request, 'accounts/register.html', {'form': form, 'new_user': user})
    else:
        form = ExtendedUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required(login_url="/accounts/login")
def view_profile(request, user_id):
    user = logic.get_user_or_404(pk=user_id)
    return render(request, 'accounts/view_profile.html', {
        'user': user, 
        'recent_matches': get_players_match_feed(user, Ladder.objects.get(pk=1)), 
        'watched_feed': map(lambda l: (l, l.watcher(user)), map(lambda p: p.ladder, Watcher.objects.filter(user=user))),
    })

@login_required(login_url="/accounts/login")
def edit_profile(request, user_id):
    return render(request, 'accounts/edit_profile.html')
