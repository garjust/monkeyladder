from django.shortcuts import redirect, render

from core import logic
from core.forms import LadderConfigurationForm
from leaderboard.forms import LeaderboardConfigurationForm

import leaderboard.contexts

VIEW = 'view'
CONTENT = 'content'
CONFIG = 'configure'

EMPTY_CONTEXT_FUNCTION = lambda *args, **kwargs: {}

CONTEXTS = {
    'BASIC': {
        VIEW: (EMPTY_CONTEXT_FUNCTION, 'core/view_ladder.html'),
        CONTENT: (EMPTY_CONTEXT_FUNCTION, 'core/content/ladder_display.html'),
        CONFIG: (LadderConfigurationForm, 'core/configure_ladder.html'),
    },
    'LEADERBOARD' : {
        VIEW: (leaderboard.contexts.view_ladder_context, 'leaderboard/view_ladder.html'),
        CONTENT: (leaderboard.contexts.ladder_display_context, 'core/content/ladder_display.html'),
        CONFIG: (LeaderboardConfigurationForm, 'leaderboard/configure_ladder.html'),
    }
}

def view_ladder(request, ladder_id):
    ladder = logic.get_ladder_or_404(pk=ladder_id)
    if not logic.can_view_ladder(request.user, ladder):
        return redirect('/home')
    context = {
        'navbar_active': 'ladder',
        'ladder': ladder,
        'watcher': logic.get_watcher(request.user, ladder)
    }
    context.update(CONTEXTS[ladder.type][VIEW][0](request, ladder))
    return render(request, CONTEXTS[ladder.type][VIEW][1], context)

def ladder_display(request, ladder_id, context={}):
    ladder = logic.get_ladder_or_404(pk=ladder_id)
    if not logic.can_view_ladder(request.user, ladder):
        return redirect('/home')
    context.update({
        'ladder': ladder,
        'watcher': logic.get_watcher(request.user, ladder)
    })
    context.update(CONTEXTS[ladder.type][CONTENT][0](request, ladder))
    return render(request, CONTEXTS[ladder.type][CONTENT][1], context)

def configure_ladder(request, ladder_id):
    ladder = logic.get_ladder_or_404(pk=ladder_id)
    form_class =  CONTEXTS[ladder.type][CONFIG][0]
    if request.POST:
        form = form_class(ladder, request.POST)
        if form.is_valid():
            form.save()
            return redirect(ladder)
    else:
        form = form_class(ladder)
    context = {
        'navbar_active': 'config',
        'ladder': ladder,
        'watcher': logic.get_watcher(request.user, ladder),
        'form': form,
    }
    return render(request, CONTEXTS[ladder.type][CONFIG][1], context)