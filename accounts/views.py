from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, render
from django.template import RequestContext

from accounts.forms import ExtendedUserCreationForm
from core.models import Ladder
from leaderboard.models import Player
from leaderboard.logic import get_players_match_feed

def register(request):
    if request.POST:
        return _do_registration(request)
    return render_to_response('accounts/register.html',
        {'form': ExtendedUserCreationForm()},
        context_instance=RequestContext(request)
    )

def _do_registration(request):
    form = ExtendedUserCreationForm(request.POST)
    if form.is_valid():
        user = form.save(commit=True)
        form = ExtendedUserCreationForm()
        form.success = True
    return render_to_response('accounts/register.html',
        {'form': form},
        context_instance=RequestContext(request)
    )

@login_required(login_url="/accounts/login")
def profile(request):
    return render(request, 'accounts/profile.html', {'recent_matches': get_players_match_feed(request.user, Ladder.objects.get(pk=1)), 'ladders': map(lambda p: p.ladder, Player.objects.filter(user=request.user))})

@login_required(login_url="/accounts/login")
def edit_profile(request):
    return render_to_response('accounts/edit_profile.html',
        {},
        context_instance=RequestContext(request)
    )
