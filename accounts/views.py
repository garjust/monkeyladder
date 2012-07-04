from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

from accounts.forms import ExtendedUserCreationForm
from core.models import Ladder, Player

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
        ladder = Ladder.objects.filter(name="Points Ping Pong")
        if ladder:
            ladder = ladder[0]
            Player(ladder=ladder, user=user, rank=len(Player.objects.filter(ladder=ladder)) + 1).save()
    return render_to_response('accounts/register.html',
        {'form': form},
        context_instance=RequestContext(request)
    )

@login_required(login_url="/accounts/login")
def profile(request):
    return render_to_response('accounts/profile.html',
        {},
        context_instance=RequestContext(request)
    )
    
@login_required(login_url="/accounts/login")
def edit_profile(request):
    return render_to_response('accounts/edit_profile.html',
        {},
        context_instance=RequestContext(request)
    )