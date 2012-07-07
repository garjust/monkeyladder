from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.http import HttpResponseForbidden

from django.contrib.admin.models import User
from core.models import Ladder, Player, Watcher

from core.logic import get_ladder_context, has_ladder_permission

@login_required(login_url="/accounts/login")
def create(request):
    newest_ladders = Ladder.objects.filter(is_private=False).order_by('-created')[:10]
    private_ladders = []
    if request.user.is_authenticated():
        private_ladders = filter(lambda l: has_ladder_permission(request.user, l), Ladder.objects.filter(is_private=True).order_by('-created'))
    return render_to_response(
        'ladders/home.html',
        {'newest_ladders': newest_ladders, 'private_ladders': private_ladders, 'navbar_active': 'home'},
        context_instance=RequestContext(request),
    )

def ladder(request, ladder_id):
    ladder = get_object_or_404(Ladder, pk=ladder_id)
    if ladder.is_private:
        if not has_ladder_permission(request.user, ladder):
            return HttpResponseForbidden()
    return render_to_response(
        'ladders/ladder.html',
        get_ladder_context(ladder),
        context_instance=RequestContext(request),
    )
    
def watchers(request, ladder_id):
    ladder = get_object_or_404(Ladder, pk=ladder_id)
    watchers = ladder.watcher_set.filter()
    return render_to_response(
        'ladders/watchers.html',
        {'navbar_active': 'watchers', 'ladder': ladder, 'watchers': watchers},
        context_instance=RequestContext(request),
    )
    
@login_required(login_url='/accounts/login/')
def watched(request):
    watchers = Watcher.objects.filter(user=User.objects.filter(pk=request.user.id))
    return render_to_response(
        'ladders/watched.html',
        {'watchers': watchers, 'navbar_active': 'watching'},
        context_instance=RequestContext(request),
    )

@login_required(login_url='/accounts/login/')
def climbing(request):
    players = Player.objects.filter(user=User.objects.filter(pk=request.user.id))
    return render_to_response(
        'ladders/climbing.html',
        {'players': players, 'navbar_active': 'climbing'},
        context_instance=RequestContext(request),
    )