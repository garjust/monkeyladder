from matches.views import leaderboard

def ladder_template_delegator(request, ladder):
    """
    Delegates rendering of a ladder based on the ladders type
    """
    FUNCTION_MAPPING = {
        'BASIC': leaderboard,
        'LEADERBOARD': leaderboard,
    }
    return FUNCTION_MAPPING[ladder.type](request, ladder)