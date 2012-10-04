from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from core import logic, views_ladder
from core.decorators import can_view_ladder, login_required_and_ladder_admin
from core.forms import LadderCreationForm, LadderRankingEditForm
from leaderboard.forms import LadderRankingAndPlayerEditForm

@login_required
def feeds(request):
    return render(request, 'core/feeds.html', {'ladder_feed_size': 4, 'navbar_active': 'feeds',
        'watched_ladder_feed': logic.nonfavorite_ladder_feed(request.user, size=25),
        'favorite_ladder_feed': logic.favorite_ladder_feed(request.user, size=25),
        'public_ladder_feed': logic.public_ladder_feed(request.user, size=25),
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

@login_required_and_ladder_admin
def edit_ladder(request, ladder_id):
    ladder = logic.get_ladder_or_404(pk=ladder_id)

    # IM IN A RUSH
    form_class = LadderRankingEditForm
    if ladder.type == 'LEADERBOARD':
        form_class = LadderRankingAndPlayerEditForm

    if request.POST:
        form = form_class(ladder, request.POST)
        if form.is_valid():
            form.save()
            return redirect(ladder)
    else:
        form = form_class(ladder)
    return views_ladder.ladder_display(request, ladder_id, context={'ladder_edit_form': form})

@can_view_ladder
def view_watchers(request, ladder_id):
    ladder = logic.get_ladder_or_404(pk=ladder_id)
    return render(request, 'core/view_ladder_watchers.html', logic.get_base_ladder_context(request, ladder, {
        'navbar_active': 'watchers', 'watcher_feed': logic.ladder_watchers(ladder)
    }))

@can_view_ladder
def watch_ladder(request, ladder_id):
    ladder = logic.get_ladder_or_404(pk=ladder_id)
    logic.create_watcher(ladder, request.user, request.user)
    return redirect(ladder)
