from django.shortcuts import render_to_response
from django.template import RequestContext

from core.models import Ladder

def home(request):
    public_ladder_feed = Ladder.objects.filter(is_private=False).order_by('-created')[:5]
    watched_ladder_feed = Ladder.objects.filter(is_private=True).order_by('-created')[:5]
    return render_to_response(
        'home.html',
        {'public_ladder_feed': public_ladder_feed, 'watched_ladder_feed': watched_ladder_feed},
        context_instance=RequestContext(request),
    )