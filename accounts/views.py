from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from accounts import logic
from accounts.forms import ExtendedUserCreationForm
from core.logic import watched_ladder_feed
from leaderboard.logic import get_players_match_feed, count_players_matches, count_players_wins

def register(request):
    if request.POST:
        form = ExtendedUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/home/")
    else:
        form = ExtendedUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required(login_url="/accounts/login")
def view_profile(request, user_id):
    user = logic.get_user_or_404(pk=user_id)
    return render(request, 'accounts/view_profile.html', {
        'user': user,
        'recent_matches': get_players_match_feed(user),
        'watched_feed': watched_ladder_feed(user, include_watchers=True),
        'matches_won': count_players_wins(user),
        'matches_played': count_players_matches(user),
    })

@login_required(login_url="/accounts/login")
def edit_profile(request, user_id):
    return render(request, 'accounts/edit_profile.html')
