from django.shortcuts import render_to_response
from django.template import RequestContext

from core.models import Ladder
from core.logic import watched_ladder_feed

def home(request):
    public_ladder_feed = Ladder.objects.filter(is_private=False).order_by('-created')[:5]
    return render_to_response(
        'home.html',
        {'public_ladder_feed': public_ladder_feed, 'watched_ladder_feed': watched_ladder_feed(request.user)},
        context_instance=RequestContext(request),
    )