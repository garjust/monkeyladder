from core import logic

import core.views
import leaderboard.views

VIEW = 'view'
CONTENT = 'content'
WATCHERS = 'watchers'
EDIT = 'edit'
WATCH = 'watch'

FUNCTION_MAPPING = {
    'BASIC': {
        VIEW: core.views.view_ladder,
        CONTENT: leaderboard.views.ladder_display_content,
        WATCHERS: core.views.view_ladder_watchers,
        EDIT: leaderboard.views.edit_ladder,
    },
    'LEADERBOARD': {
        VIEW: leaderboard.views.view_ladder,
        CONTENT: leaderboard.views.ladder_display_content,
        WATCHERS: core.views.view_ladder_watchers,
        EDIT: leaderboard.views.edit_ladder,
    }
}

def delegate_ladder_view(request, ladder_id):
    """
    Delegates rendering of a ladders page
    """
    ladder = logic.get_ladder_or_404(pk=ladder_id)
    return FUNCTION_MAPPING[ladder.type][VIEW](request, ladder_id)

def delegate_ladder_content(request, ladder_id):
    """
    Delegates rendering of a ladders content
    """
    ladder = logic.get_ladder_or_404(pk=ladder_id)
    return FUNCTION_MAPPING[ladder.type][CONTENT](request, ladder_id)

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
    return FUNCTION_MAPPING[ladder.type][EDIT](request, ladder_id)

def delegate_watch_ladder(request, ladder_id):
    ladder = logic.get_ladder_or_404(pk=ladder_id)
    return FUNCTION_MAPPING[ladder.type][WATCH](request, ladder_id)
