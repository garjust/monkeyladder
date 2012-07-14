from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from core.models import LadderPermission
from core import logic
from core import delegator
from core.forms import LadderCreationForm

@login_required
def activity(request):
    return render(request, 'core/full/activity.html',
        {'watched_ladder_feed': logic.watched_ladder_feed(request.user, size=25), 'favorite_ladder_feed': logic.favorite_ladder_feed(request.user, size=25),
         'public_ladder_feed': logic.public_ladder_feed(request.user, size=25), 'ladder_feed_size': 4, 'navbar_active': 'activity'})

def view_ladder(request, ladder_id):
    ladder = logic.get_ladder_or_404(pk=ladder_id)
    if not logic.can_view_ladder(request.user, ladder):
        return redirect('/home')
    return delegator.ladder_template_delegator(request, ladder)

@login_required
def create_ladder(request):
    if request.POST:
        form = LadderCreationForm(request.POST)
        if form.is_valid():
            ladder, ladder_admin = form.save(commit=True)
            ladder_admin.admin = True
            perm = LadderPermission(ladder=ladder, watcher=ladder_admin, type='ADMIN')
            perm.save()
            form = LadderCreationForm()
            return redirect('/ladders/{}'.format(ladder.id))
    else:
        form = LadderCreationForm()
    return render(request, 'core/full/create.html', {'form': form})

def watchers(request, ladder_id):
    ladder = logic.get_ladder_or_404(pk=ladder_id)
    return render(request, 'core/full/watchers.html', {'navbar_active': 'watchers', 'ladder': ladder, 'watcher_feed': logic.ladder_watchers(ladder)})
    
def ladder_display_content(request, ladder_id):
    ladder = logic.get_ladder_or_404(pk=ladder_id)
    return delegator.ladder_content_delegator(request, ladder)

def ladder_creation_form_content(request):
    form = LadderCreationForm()
    return render(request, 'core/ladder_creation_form.html', {'form': form})
