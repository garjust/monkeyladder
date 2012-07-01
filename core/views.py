from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from django.contrib.admin.models import User
from core.models import Ladder, Player, Watcher

from core.logic import LadderPlayerAutocomplete

def home(request):
    newest_ladders = Ladder.objects.filter(is_private=False).order_by('-created')[:50]
    return render_to_response(
        'ladders/home.html',
        {'newest_ladders': newest_ladders, 'navbar_active': 'home'},
        context_instance=RequestContext(request),
    )

def ladder(request, ladder_id):
    ladder = get_object_or_404(Ladder, pk=ladder_id)
    if ladder.is_private:
        if not request.user.is_authenticated() or (len(ladder.player_set.filter(user=request.user)) == 0 and len(ladder.watcher_set.filter(user=request.user)) == 0):
            raise Exception() 
    return render_to_response(
        'ladders/ladder.html',
        {'navbar_active': 'ladder', 'ladder': ladder, 'players': ladder.ranking(), 'player_names': LadderPlayerAutocomplete().get_autocomplete_list(ladder)},
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
        {'watchers': watchers, 'navbar_active': 'watched'},
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