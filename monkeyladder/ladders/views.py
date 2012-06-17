from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import Context, loader

from ladders.models import Ladder

def home(request):
    newest_ladders = Ladder.objects.all().order_by('-created')[:5]
    return render_to_response('ladders/home.html', {'newest_ladders': newest_ladders, 'navbar_active': 'home'})

def watched(request):
    return render_to_response('ladders/watched.html', {'navbar_active': 'watched'})

def climbing(request):
    return render_to_response('ladders/climbing.html', {'navbar_active': 'climbing'})

def ladder(request, ladder_id):
    ladder = get_object_or_404(Ladder, pk=ladder_id)
    ladder_users = ladder.ladderuser_set.filter().order_by('rank')
    return render_to_response('ladders/ladder.html', {'ladder': ladder, 'ladder_users': ladder_users})

def update(request, ladder_id):
    return HttpResponse("Attempt to change ladder {}".format(ladder_id))