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
        VIEW: {'context': EMPTY_CONTEXT_FUNCTION, 'template': 'core/view_ladder.html'},
        CONTENT: {'context': EMPTY_CONTEXT_FUNCTION, 'template': 'core/content/ladder_display.html'},
        CONFIG: {'form': LadderConfigurationForm, 'template': 'core/configure_ladder.html'},
    },
    'LEADERBOARD' : {
        VIEW: {'context': leaderboard.contexts.view_ladder_context, 'template': 'leaderboard/view_ladder.html'},
        CONTENT: {'context': leaderboard.contexts.ladder_display_context, 'template': 'core/content/ladder_display.html'},
        CONFIG: {'form': LeaderboardConfigurationForm, 'template': 'leaderboard/configure_ladder.html'},
    }
}

def view_ladder(request, ladder_id):
    ladder = logic.get_ladder_or_404(pk=ladder_id)
    if not logic.can_view_ladder(request.user, ladder):
        return redirect('/home')
    context = logic.get_base_ladder_context(request, ladder)
    context.update({'navbar_active': 'ladder'})
    context.update(CONTEXTS[ladder.type][VIEW]['context'](request, ladder))
    return render(request, CONTEXTS[ladder.type][VIEW]['template'], context)

def ladder_display(request, ladder_id, context={}):
    ladder = logic.get_ladder_or_404(pk=ladder_id)
    if not logic.can_view_ladder(request.user, ladder):
        return redirect('/home')
    context.update(logic.get_base_ladder_context(request, ladder))
    context.update(CONTEXTS[ladder.type][CONTENT]['context'](request, ladder))
    return render(request, CONTEXTS[ladder.type][CONTENT]['template'], context)

def configure_ladder(request, ladder_id):
    ladder = logic.get_ladder_or_404(pk=ladder_id)
    form_class = CONTEXTS[ladder.type][CONFIG]['form']
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
    return render(request, CONTEXTS[ladder.type][CONFIG]['template'], context)
