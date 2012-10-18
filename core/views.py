from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from core import logic
from core.decorators import can_view_ladder, login_required_and_ladder_admin
from core.forms import LadderCreationForm, LadderRankingEditForm, LadderConfigurationForm
from core.generic_views import handle_form_and_redirect_to_ladder, view_with_ladder

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
    logic.util.create_watcher(ladder, request.user, request.user)
    return redirect(ladder)

@can_view_ladder
def view_ladder(request, ladder_id):
    ladder = logic.util.get_ladder_or_404(pk=ladder_id)
    return view_with_ladder(request, ladder, 'core/view_ladder.html', {'navbar_active': 'ladder'})

@can_view_ladder
def ladder_display(request, ladder_id):
    ladder = logic.util.get_ladder_or_404(pk=ladder_id)
    return view_with_ladder(request, ladder, 'core/content/ladder_display.html')

@login_required_and_ladder_admin
def edit_ladder(request, ladder_id):
    return handle_form_and_redirect_to_ladder(request, ladder_id, LadderRankingEditForm, 'core/content/ladder_display.html',
        form_name='ladder_edit_form'
    )

@login_required_and_ladder_admin
def configure_ladder(request, ladder_id):
    return handle_form_and_redirect_to_ladder(request, ladder_id, LadderConfigurationForm, 'core/configure_ladder.html',
        context={'navbar_active': 'config'}
    )
