from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.http import HttpResponseForbidden

from django.contrib.admin.models import User
from matches.models import Player
from core.models import Ladder, Ranked, Watcher

from core.logic import has_ladder_permission, watched_ladder_feed, favorite_ladder_feed, public_ladder_feed
    

from matches.views import leaderboard

def ladder(request, ladder_id):
    ladder = get_object_or_404(Ladder, pk=ladder_id)
    if ladder.is_private:
        if not has_ladder_permission(request.user, ladder):
            return HttpResponseForbidden()
    if ladder.type == 'BASIC':
        pass
    elif ladder.type == 'LEADERBOARD':
        return leaderboard(request, ladder)

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
    
def watchers(request, ladder_id):
    ladder = get_object_or_404(Ladder, pk=ladder_id)
    watchers = ladder.watcher_set.filter()
    return render_to_response(
        'ladders/watchers.html',
        {'navbar_active': 'watchers', 'ladder': ladder, 'watchers': watchers},
        context_instance=RequestContext(request),
    )
    
@login_required(login_url='/accounts/login')
def activity(request):
    public = public_ladder_feed(request.user, size=25)
    watching = watched_ladder_feed(request.user, size=25)
    favorites = favorite_ladder_feed(request.user, size=25)
    return render_to_response(
        'ladders/activity.html',
        {
            'watched_ladder_feed': watching, 'favorite_ladder_feed': favorites, 'public_ladder_feed': public, 
            'ladder_feed_size': 4, 'navbar_active': 'activity'
        },
        context_instance=RequestContext(request),
    )