from django.shortcuts import render

from core.logic import watched_ladder_feed, public_ladder_feed

def home(request):
    return render(request, 'home.html', {
        'public_ladder_feed': public_ladder_feed(request.user),
        'watched_ladder_feed': watched_ladder_feed(request.user),
        'navbar_active': 'home'
    })
