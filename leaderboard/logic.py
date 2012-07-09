from core.models import Ranked
from leaderboard.models import Match, Player

import logging
logger = logging.getLogger('monkeyladder')

def get_match_feed(ladder, order='-created', size=5):
    """
    Returns a match feed for the specified ladder
    """
    return Match.objects.filter(ladder=ladder).order_by(order)[:size]

def climbing_ladder_feed(user, order='-created', size=5):
    """
    Returns a ladder feed of the ladders the user is climbing
    """
    if user.is_authenticated():
        return map(lambda p: p.ladder, user.player_set.all().order_by(order)[:size])

def get_autocomplete_list(ladder):
    """
    Returns a list of names of players on the given ladder
    """
    rankeds = ladder.ranked_set.order_by('rank')
    names = []
    for ranked in rankeds:
        player = ranked.player
        names.append(player.user.get_profile().name())
    return _format_names_for_injection(names)

def _format_names_for_injection(names):
    """
    Formats the list of names into a string that can be injected into javascript
    """
    return ','.join(map(lambda n: '"{}"'.format(n), names))

def get_ladder_context(ladder, *partial_contexts):
    context = {'navbar_active': 'ladder', 'ladder': ladder, 'player_names': get_autocomplete_list(ladder), 'match_feed': get_match_feed(ladder)}
    for partial_context in partial_contexts:
        context.update(partial_context)
    return context
    
def get_ladder_player_dictionary(ladder):
        player_dictionary = {}
        for ranked in ladder.ranking():
            player_dictionary[ranked.player.user.get_profile().name()] = ranked.player.user
        return player_dictionary
  
def adjust_rankings(match):
    winner = Ranked.objects.get(ladder=match.ladder, rank=Player.objects.get(user=match.winner, ladder=match.ladder).rank)
    loser = Ranked.objects.get(ladder=match.ladder, rank=Player.objects.get(user=match.loser, ladder=match.ladder).rank)
    players = list(match.ladder.ranking())
    rank_diff = winner.rank - loser.rank
    if rank_diff <= 0:
        print "No change"
    elif rank_diff <= 2:
        print "Players are close, doing swap"
        loser_old_rank = loser.rank
        loser.rank = winner.rank
        winner.rank = loser_old_rank
    else:
        print "Players are far, each move one towards each other"
        below_loser = players[players.index(loser) + 1]
        below_loser_rank = below_loser.rank
        below_loser.rank = loser.rank
        loser.rank = below_loser_rank

        above_winner = players[players.index(winner) - 1]
        above_winner_rank = above_winner.rank
        above_winner.rank = winner.rank
        winner.rank =above_winner_rank
        
        above_winner.save()
        below_loser.save()
    winner.save()
    loser.save()