from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render_to_response, render, redirect
from django.template import RequestContext

from core import logic
from core.delegator import ladder_template_delegator, ladder_ajax_delegator
from core.forms import LadderCreationForm

@login_required
def activity(request):
    return render_to_response(
        'core/full/activity.html',
        {
            'watched_ladder_feed': logic.watched_ladder_feed(request.user, size=25),
            'favorite_ladder_feed': logic.favorite_ladder_feed(request.user, size=25),
            'public_ladder_feed': logic.public_ladder_feed(request.user, size=25),
            'ladder_feed_size': 4, 'navbar_active': 'activity'
        },
        context_instance=RequestContext(request),
    )

def ladder(request, ladder_id):
    ladder = logic.get_ladder_or_404(pk=ladder_id)
    if ladder.is_private and not logic.can_view_ladder(request.user, ladder):
        return HttpResponseForbidden()
    return ladder_template_delegator(request, ladder)

def ladder_display_content(request, ladder_id):
    ladder = logic.get_ladder_or_404(pk=ladder_id)
    return ladder_ajax_delegator(request, ladder)

def ladder_creation_form_content(request):
    form = LadderCreationForm()
    return render(request, 'core/ladder_creation_form.html', {'form': form})

@login_required
def create(request):
    if request.POST:
        form = LadderCreationForm(request.POST)
        if form.is_valid():
            ladder, ladder_admin = form.save(commit=True)
            ladder_admin.admin = True
            ladder_admin.save()
            form = LadderCreationForm()
            return redirect('/ladders/{}'.format(ladder.id))
    else:
        form = LadderCreationForm()
    return render(request, 'core/full/create.html', {'form': form})

def watchers(request, ladder_id):
    ladder = logic.get_ladder_or_404(pk=ladder_id)
    return render_to_response(
        'core/full/watchers.html',
        {'navbar_active': 'watchers', 'ladder': ladder, 'watcher_feed': logic.ladder_watchers(ladder)},
        context_instance=RequestContext(request),
    )
