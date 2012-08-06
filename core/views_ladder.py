from django.shortcuts import redirect, render

from core import logic
from core.decorators import can_view_ladder, login_required_and_ladder_admin
from core.forms import LadderConfigurationForm

import leaderboard

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
        CONTENT: {'context': leaderboard.contexts.ladder_display_context, 'template': 'leaderboard/content/ladder_display.html'},
        CONFIG: {'form': leaderboard.forms.LeaderboardConfigurationForm, 'template': 'leaderboard/configure_ladder.html'},
    }
}

@can_view_ladder
def view_ladder(request, ladder_id):
    ladder = logic.get_ladder_or_404(pk=ladder_id)
    context = logic.get_base_ladder_context(request, ladder, extra={'navbar_active': 'ladder'})
    context.update(CONTEXTS[ladder.type][VIEW]['context'](request, ladder))
    return render(request, CONTEXTS[ladder.type][VIEW]['template'], context)

@can_view_ladder
def ladder_display(request, ladder_id, context={}):
    ladder = logic.get_ladder_or_404(pk=ladder_id)
    context = logic.get_base_ladder_context(request, ladder, extra=context)
    context.update(CONTEXTS[ladder.type][CONTENT]['context'](request, ladder))
    return render(request, CONTEXTS[ladder.type][CONTENT]['template'], context)

@login_required_and_ladder_admin
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
    context = logic.get_base_ladder_context(request, ladder, extra={'navbar_active': 'config', 'form': form})
    return render(request, CONTEXTS[ladder.type][CONFIG]['template'], context)
