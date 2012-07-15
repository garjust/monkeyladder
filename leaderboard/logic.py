from core.models import Ranked
from leaderboard.models import Match, Player

import logging
logger = logging.getLogger('monkeyladder')

def get_match_feed(ladder, order='-created', size=5):
    """
    Returns a match feed for the specified ladder
    """
    return Match.objects.filter(ladder=ladder).order_by(order)[:size]

def get_players_match_feed(user, ladder, order='-created', size=5):
    """
    Returns a match feed for the specified ladder with only matches with the given user
    """
    return (Match.objects.filter(ladder=ladder, winner=user) | Match.objects.filter(ladder=ladder, loser=user)).order_by(order)[:size]

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

def get_ladder_player_dictionary(ladder):
    """
    Returns a dictionary with the names of a ladders players as keys and the user instance as values
    """
    player_dictionary = {}
    for ranked in ladder.ranking():
        player_dictionary[ranked.player.user.get_profile().name()] = ranked.player.user
    return player_dictionary

def inverse_match(match):
    return Match(ladder=match.ladder,
        winner=match.loser, winner_score=match.loser_score,
        loser=match.winner, loser_score=match.winner_score,
        created=match.created, ranking_change=match.ranking_change
    )

def delete_match(match):
    pass

SWAP_RANGE = 2
ADVANCEMENT_RANKS = 2
AUTO_TAKE_FIRST = True

def adjust_rankings(match):
    if not match.ranking_change:
        return
    winner = Ranked.objects.get(ladder=match.ladder, rank=Player.objects.get(user=match.winner, ladder=match.ladder).rank)
    loser = Ranked.objects.get(ladder=match.ladder, rank=Player.objects.get(user=match.loser, ladder=match.ladder).rank)
    players = list(match.ladder.ranking())
    rank_diff = winner.rank - loser.rank
    if rank_diff <= 0:
        pass
    elif rank_diff <= SWAP_RANGE:
        loser_old_rank = loser.rank
        loser.rank = winner.rank
        winner.rank = loser_old_rank
        winner.save()
        loser.save()
    else:
        if AUTO_TAKE_FIRST and loser.rank == 1:
            adjustment = rank_diff + 1
        elif rank_diff <= ADVANCEMENT_RANKS:
            adjustment = rank_diff + 1
        else:
            adjustment = ADVANCEMENT_RANKS + 1
        player_slice = players[winner.rank-adjustment:winner.rank]
        player_slice[-1].rank = player_slice[0].rank
        player_slice[-1].save()
        player_slice = player_slice[:-1]
        for player in player_slice:
            player.rank += 1
            player.save()