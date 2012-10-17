from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from core import logic
from core.decorators import can_view_ladder, login_required_and_ladder_admin
from core.forms import LadderCreationForm, LadderRankingEditForm, LadderConfigurationForm

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

@login_required_and_ladder_admin
def edit_ladder(request, ladder_id):
    ladder = logic.util.get_ladder_or_404(pk=ladder_id)
    if request.POST:
        form = LadderRankingEditForm(ladder, request.POST)
        if form.is_valid():
            form.save()
            return redirect(ladder)
    else:
        form = LadderRankingEditForm(ladder)
    return ladder_display(request, ladder_id, context={'ladder_edit_form': form})

@can_view_ladder
def view_watchers(request, ladder_id):
    ladder = logic.util.get_ladder_or_404(pk=ladder_id)
    return render(request, 'core/view_ladder_watchers.html', logic.util.get_base_ladder_context(request, ladder, {
        'navbar_active': 'watchers', 'watcher_feed': logic.util.ladder_watchers(ladder)
    }))

@can_view_ladder
def watch_ladder(request, ladder_id):
    ladder = logic.util.get_ladder_or_404(pk=ladder_id)
    logic.util.create_watcher(ladder, request.user, request.user)
    return redirect(ladder)

@can_view_ladder
def view_ladder(request, ladder_id):
    ladder = logic.util.get_ladder_or_404(pk=ladder_id)
    context = logic.util.get_base_ladder_context(request, ladder, extra={'navbar_active': 'ladder'})
    return render(request, 'core/view_ladder.html', context)

@can_view_ladder
def ladder_display(request, ladder_id, context=None):
    if not context:
        context = {}
    ladder = logic.util.get_ladder_or_404(pk=ladder_id)
    context = logic.util.get_base_ladder_context(request, ladder, extra=context)
    return render(request, 'core/content/ladder_display.html', context)

@login_required_and_ladder_admin
def configure_ladder(request, ladder_id):
    ladder = logic.util.get_ladder_or_404(pk=ladder_id)
    if request.POST:
        form = LadderConfigurationForm(ladder, request.POST)
        if form.is_valid():
            form.save()
            return redirect(ladder)
    else:
        form = LadderConfigurationForm(ladder)
    context = logic.util.get_base_ladder_context(request, ladder, extra={'navbar_active': 'config', 'form': form})
    return render(request, 'core/configure_ladder.html', context)
