from core.forms import LadderCreationForm
from core.logic.feeds import watched_ladder_feed, public_ladder_feed, nonfavorite_ladder_feed, favorite_ladder_feed
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


def home_page(request):
    return render(request, 'home.html', {'navbar_active': 'home',
        'public_ladder_feed': public_ladder_feed(request.user),
        'watched_ladder_feed': watched_ladder_feed(request.user),
    })


@login_required
def feeds_page(request):
    return render(request, 'core/feeds.html', {'navbar_active': 'feeds', 'ladder_feed_size': 4,
        'public_ladder_feed': public_ladder_feed(request.user, size=25),
        'watched_ladder_feed': nonfavorite_ladder_feed(request.user, size=25),
        'favorite_ladder_feed': favorite_ladder_feed(request.user, size=25),
    })


@login_required
def create_ladder_page(request):
    if request.POST:
        form = LadderCreationForm(request.POST)
        if form.is_valid():
            ladder = form.save(request.user)
            return redirect(ladder)
    else:
        form = LadderCreationForm()
    return render(request, 'core/create_ladder.html', {'form': form})
