from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from core import logic
from core.forms import LadderCreationForm

from core.models import Watcher

@login_required
def feeds(request):
    return render(request, 'core/feeds.html', {'ladder_feed_size': 4, 'navbar_active': 'feeds',
        'watched_ladder_feed': logic.watched_ladder_feed(request.user, size=25),
        'favorite_ladder_feed': logic.favorite_ladder_feed(request.user, size=25),
        'public_ladder_feed': logic.public_ladder_feed(request.user, size=25),
    })

@login_required
def create_ladder(request):
    if request.POST:
        form = LadderCreationForm(request.user, request.POST)
        if form.is_valid():
            ladder = form.save()
            return redirect(ladder)
    else:
        form = LadderCreationForm(request.user)
    return render(request, 'core/create_ladder.html', {'form': form})

def view_ladder(request, ladder_id, context={}):
    ladder = logic.get_ladder_or_404(pk=ladder_id)
    return render(request, 'core/view_ladder.html', context)

def view_ladder_watchers(request, ladder_id):
    ladder = logic.get_ladder_or_404(pk=ladder_id)
    if not logic.can_view_ladder(request.user, ladder):
        return redirect('/home')
    return render(request, 'core/view_ladder_watchers.html', {'navbar_active': 'watchers', 'ladder': ladder, 'watcher_feed': logic.ladder_watchers(ladder)})

@login_required
def watch_ladder(request, ladder_id):
    ladder = logic.get_ladder_or_404(pk=ladder_id)
    if logic.can_view_ladder(request.user, ladder):
        Watcher.objects.create(ladder=ladder, user=request.user)
    return redirect(ladder)
