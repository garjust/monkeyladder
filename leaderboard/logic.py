from django.utils import timezone

from core.models import Ranked, RankingChange
from leaderboard.models import Match, Player, MatchRankingChangeSet

import logging
logger = logging.getLogger('monkeyladder')

def get_match_feed(ladder, order='-created', size=10):
    """
    Returns a match feed for the specified ladder
    """
    return Match.objects.filter(ladder=ladder).order_by(order)[:size]

def get_players_match_feed(user, ladder=None, order='-created', size=5):
    """
    Returns a match feed for the specified ladder and user
    """
    if ladder:
        return (Match.objects.filter(ladder=ladder, winner=user) | Match.objects.filter(ladder=ladder, loser=user)).order_by(order)[:size]
    return (Match.objects.filter(winner=user) | Match.objects.filter(loser=user)).order_by(order)[:size]

def count_players_wins(user, ladder=None):
    """
    Returns the users total matches won.

    If a ladder is supplied only that ladder will be considered
    """
    if ladder:
        return Match.objects.filter(ladder=ladder, winner=user).count()
    return Match.objects.filter(winner=user).count()

def count_players_losses(user, ladder=None):
    """
    Returns the users total matches lost.

    If a ladder is supplied only that ladder will be considered
    """
    if ladder:
        return Match.objects.filter(ladder=ladder, loser=user).count()
    return Match.objects.filter(loser=user).count()

def count_players_matches(user, ladder=None):
    """
    Returns the users total matches played.

    If a ladder is supplied only that ladder will be considered
    """
    return count_players_wins(user, ladder) + count_players_losses(user, ladder)

def climbing_ladder_feed(user, order='-created', size=5):
    """
    Returns a ladder feed of the ladders the user is a player on
    """
    if user.is_authenticated():
        return map(lambda p: p.ladder, user.player_set.all().order_by(order)[:size])

def get_ladder_players(ladder):
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

SWAP_RANGE = 0
ADVANCEMENT_RANKS = 2
AUTO_TAKE_FIRST = True

def adjust_rankings(match):
    if not match.ranking_change:
        return
    winner = Ranked.objects.get(ladder=match.ladder, rank=Player.objects.get(user=match.winner, ladder=match.ladder).rank)
    loser = Ranked.objects.get(ladder=match.ladder, rank=Player.objects.get(user=match.loser, ladder=match.ladder).rank)
    ranking_change_set = MatchRankingChangeSet(ladder=match.ladder, change_date=timezone.now(), match=match)
    players = list(match.ladder.ranking())
    rank_diff = winner.rank - loser.rank
    if rank_diff <= 0:
        return
    ranking_change_set.save()
    if rank_diff <= SWAP_RANGE:
        RankingChange(ranking_change_set=ranking_change_set, ranked=winner, rank=winner.rank, change= -(winner.rank - loser.rank)).save()
        RankingChange(ranking_change_set=ranking_change_set, ranked=loser, rank=loser.rank, change=winner.rank - loser.rank).save()
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
        RankingChange(ranking_change_set=ranking_change_set, ranked=winner, rank=winner.rank, change= -(adjustment - 1)).save()
        #ranking_change.winner_change = adjustment - 1
        player_slice = players[winner.rank - adjustment:winner.rank]
        player_slice[-1].rank = player_slice[0].rank
        player_slice[-1].save()
        player_slice = player_slice[:-1]
#        if loser in player_slice:
#            ranking_change.loser_change = -1
#        else:
#            ranking_change.loser_change = 0
        for player in player_slice:
            RankingChange(ranking_change_set=ranking_change_set, ranked=player, rank=player.rank, change=1).save()
            player.rank += 1
            player.save()
       # ranking_change.save()
