from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.http import HttpResponseForbidden

from django.contrib.admin.models import User
from matches.models import Player
from core.models import Ladder, Ranked, Watcher

from core.logic import has_ladder_permission, watched_ladder_feed, favorite_ladder_feed, public_ladder_feed, ladder_watchers
    

from matches.views import leaderboard

def ladder(request, ladder_id):
    ladder = get_object_or_404(Ladder, pk=ladder_id)
    if ladder.is_private:
        if not has_ladder_permission(request.user, ladder):
            return HttpResponseForbidden()
    if ladder.type == 'BASIC':
        return leaderboard(request, ladder)
    elif ladder.type == 'LEADERBOARD':
        return leaderboard(request, ladder)

@login_required(login_url="/accounts/login")
def create(request):
    if request.POST:
        return None
    return render_to_response(
        'ladders/create.html',
        {'form': None},
        context_instance=RequestContext(request),
    )
    
def watchers(request, ladder_id):
    ladder = get_object_or_404(Ladder, pk=ladder_id)
    return render_to_response(
        'ladders/watchers.html',
        {'navbar_active': 'watchers', 'ladder': ladder, 'watcher_feed': ladder_watchers(ladder)},
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