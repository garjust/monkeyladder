from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseNotAllowed
from django.shortcuts import render_to_response
from django.template import RequestContext

from core import logic
from core.delegator import ladder_template_delegator

@login_required
def activity(request):
    return render_to_response(
        'core/activity.html',
        {
            'watched_ladder_feed': logic.watched_ladder_feed(request.user, size=25), 
            'favorite_ladder_feed': logic.favorite_ladder_feed(request.user, size=25), 
            'public_ladder_feed': logic.public_ladder_feed(request.user, size=25), 
            'ladder_feed_size': 4, 'navbar_active': 'activity'
        },
        context_instance=RequestContext(request),
    )

def ladder(request, ladder_id, **kwargs):
    ladder = logic.get_ladder_or_404(pk=ladder_id)
    if ladder.is_private and not logic.can_view_ladder(request.user, ladder):
        return HttpResponseForbidden()
    return ladder_template_delegator(request, ladder, **kwargs)

@login_required
def create(request):
    if request.POST:
        return HttpResponseNotAllowed()
    return render_to_response(
        'core/create.html',
        {'form': None},
        context_instance=RequestContext(request),
    )
    
def watchers(request, ladder_id):
    ladder = logic.get_ladder_or_404(pk=ladder_id)
    return render_to_response(
        'core/watchers.html',
        {'navbar_active': 'watchers', 'ladder': ladder, 'watcher_feed': logic.ladder_watchers(ladder)},
        context_instance=RequestContext(request),
    )
