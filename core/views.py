from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from core import logic
from core.logic.feeds import watched_ladder_feed, public_ladder_feed
from core.decorators import can_view_ladder, login_required_and_ladder_admin
from core.forms import LadderCreationForm
from core.models import Watcher


def home(request):
    return render(request, 'home.html', {
        'public_ladder_feed': public_ladder_feed(request.user),
        'watched_ladder_feed': watched_ladder_feed(request.user),
        'navbar_active': 'home'
    })


@login_required
def feeds(request):
    return render(request, 'core/feeds.html', {'ladder_feed_size': 4, 'navbar_active': 'feeds',
        'watched_ladder_feed': logic.feeds.nonfavorite_ladder_feed(request.user, size=25),
        'favorite_ladder_feed': logic.feeds.favorite_ladder_feed(request.user, size=25),
        'public_ladder_feed': logic.feeds.public_ladder_feed(request.user, size=25),
    })


@login_required
def create_ladder(request):
    if request.POST:
        form = LadderCreationForm(request.POST)
        if form.is_valid():
            ladder = form.save(request.user)
            return redirect(ladder)
    else:
        form = LadderCreationForm()
    return render(request, 'core/create_ladder.html', {'form': form})


@can_view_ladder
def watch_ladder(request, ladder_id):
    ladder = logic.util.get_ladder_or_404(pk=ladder_id)
    Watcher.objects.create(ladder=ladder, user=request.user, type='NORMAL', created_by=request.user)
    return redirect(ladder)


@login_required_and_ladder_admin
def delete_ladder(request, ladder_id):
    ladder = logic.util.get_ladder_or_404(pk=ladder_id)
    ladder.is_active = False
    ladder.save()
    return redirect('/home/')
