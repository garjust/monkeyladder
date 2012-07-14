from leaderboard.views import leaderboard, ajax_ladder_display

def ladder_template_delegator(request, ladder):
    """
    Delegates rendering of a ladder based on the ladders type
    """
    FUNCTION_MAPPING = {
        'BASIC': leaderboard,
        'LEADERBOARD': leaderboard,
    }
    return FUNCTION_MAPPING[ladder.type](request, ladder)

def ladder_content_delegator(request, ladder):
    """
    Delegates rendering of a ladder based on the ladders type
    """
    FUNCTION_MAPPING = {
        'BASIC': ajax_ladder_display,
        'LEADERBOARD': ajax_ladder_display,
    }
    return FUNCTION_MAPPING[ladder.type](request, ladder)