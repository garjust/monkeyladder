from matches.views import leaderboard

def ladder_template_delegator(request, ladder):
    """
    Delegates rendering of a ladder based on the ladders type
    """
    if ladder.type == 'BASIC':
        return leaderboard(request, ladder)
    elif ladder.type == 'LEADERBOARD':
        return leaderboard(request, ladder)