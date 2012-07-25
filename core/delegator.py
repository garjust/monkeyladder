from django.shortcuts import redirect

from core import logic
from core.forms import LadderEditForm
import core.views
import leaderboard.views

VIEW = 'view'
CONTENT = 'content'
WATCHERS = 'watchers'
EDIT = 'edit'

FUNCTION_MAPPING = {
    'BASIC': {
        VIEW: core.views.view_ladder,
        CONTENT: leaderboard.views.ladder_display_content,
        WATCHERS: core.views.view_ladder_watchers,
    },
    'LEADERBOARD': {
        VIEW: leaderboard.views.view_ladder,
        CONTENT: leaderboard.views.ladder_display_content,
        WATCHERS: core.views.view_ladder_watchers,
    }
}

def delegate_ladder_view(request, ladder_id):
    """
    Delegates rendering of a ladders page
    """
    ladder = logic.get_ladder_or_404(pk=ladder_id)
    if not logic.can_view_ladder(request.user, ladder):
        return redirect('/home')
    context = {
        'navbar_active': 'ladder',
        'ladder': ladder,
        'watcher': logic.get_watcher(request.user, ladder)
    }
    return FUNCTION_MAPPING[ladder.type][VIEW](request, ladder_id, context)

def delegate_ladder_content(request, ladder_id, context={}):
    """
    Delegates rendering of a ladders content
    """
    ladder = logic.get_ladder_or_404(pk=ladder_id)
    if not logic.can_view_ladder(request.user, ladder):
        return redirect('/home')
    context.update({
        'ladder': ladder,
        'watcher': logic.get_watcher(request.user, ladder)
    })
    return FUNCTION_MAPPING[ladder.type][CONTENT](request, ladder_id, context)

def delegate_watchers_view(request, ladder_id):
    """
    Delegates rendering of a ladders watchers page
    """
    ladder = logic.get_ladder_or_404(pk=ladder_id)
    return FUNCTION_MAPPING[ladder.type][WATCHERS](request, ladder_id)

def delegate_ladder_edit(request, ladder_id):
    """
    Delegates editing of a ladder
    """
    ladder = logic.get_ladder_or_404(pk=ladder_id)
    if request.POST:
        form = LadderEditForm(ladder, request.POST)
        if form.is_valid():
            form.save(ladder)
            return redirect(ladder)
    else:
        form = LadderEditForm(ladder)
    return delegate_ladder_content(request, ladder_id, context={'ladder_edit_form': form})
