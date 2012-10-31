from core import logic
from core.decorators import can_view_ladder, login_required_and_ladder_admin, ladder_is_active
from core.forms import LadderCreationForm
from core.logic.feeds import watched_ladder_feed, public_ladder_feed, nonfavorite_ladder_feed, favorite_ladder_feed
from core.models import Watcher
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


@ladder_is_active
@can_view_ladder
def watch_ladder(request, ladder_id):
    ladder = logic.util.get_ladder_or_404(pk=ladder_id)
    Watcher.objects.create(ladder=ladder, user=request.user, type='NORMAL', created_by=request.user)
    return redirect(ladder)


@ladder_is_active
@login_required_and_ladder_admin
def delete_ladder(request, ladder_id):
    ladder = logic.util.get_ladder_or_404(pk=ladder_id)
    ladder.is_active = False
    ladder.save()
    return redirect('/home/')
