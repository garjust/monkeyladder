from leaderboard.views import leaderboard, ajax_ladder_display

TEMPLATE_KEY = 'template'
CONTENT_KEY = 'content'

FUNCTION_MAPPING = {
    'BASIC': {
        TEMPLATE_KEY: leaderboard,
        CONTENT_KEY: ajax_ladder_display
    },
    'LEADERBOARD': {
        TEMPLATE_KEY: leaderboard,
        CONTENT_KEY: ajax_ladder_display            
    }
}

def ladder_template_delegator(request, ladder):
    """
    Delegates rendering of a ladder based on the ladders type
    """
    return FUNCTION_MAPPING[ladder.type][TEMPLATE_KEY](request, ladder)

def ladder_content_delegator(request, ladder):
    """
    Delegates rendering of a ladder based on the ladders type
    """
    return FUNCTION_MAPPING[ladder.type][CONTENT_KEY](request, ladder)