from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render_to_response
from django.template import RequestContext

from core import logic
from core.delegator import ladder_template_delegator

@login_required(login_url='/accounts/login')
def activity(request):
    public = logic.public_ladder_feed(request.user, size=25)
    watching = logic.watched_ladder_feed(request.user, size=25)
    favorites = logic.favorite_ladder_feed(request.user, size=25)
    return render_to_response(
        'ladders/activity.html',
        {
            'watched_ladder_feed': watching, 'favorite_ladder_feed': favorites, 'public_ladder_feed': public, 
            'ladder_feed_size': 4, 'navbar_active': 'activity'
        },
        context_instance=RequestContext(request),
    )

def ladder(request, ladder_id):
    ladder = logic.get_ladder_or_404(pk=ladder_id)
    if ladder.is_private:
        if not logic.has_ladder_permission(request.user, ladder):
            return HttpResponseForbidden()
    return ladder_template_delegator(request, ladder)

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
    ladder = logic.get_ladder_or_404(pk=ladder_id)
    return render_to_response(
        'ladders/watchers.html',
        {'navbar_active': 'watchers', 'ladder': ladder, 'watcher_feed': logic.ladder_watchers(ladder)},
        context_instance=RequestContext(request),
    )
    
