from django.utils import timezone

from core.models import Ranked, RankingChange
from core.logic import get_config
from leaderboard.models import Player, MatchRankingChangeSet

import logging
logger = logging.getLogger('monkeyladder')

def get_ladder_players(ladder):
    """
    Returns a dictionary with the names of a ladders players as keys and the user instance as values
    """
    player_dictionary = {}
    for ranked in ladder.ranking():
        player_dictionary[ranked.player.user.get_profile().name()] = ranked.player.user
    return player_dictionary

def get_ladder_players_for_match_entry(ladder):
    """
    Returns a string of player names for use in javascript
    """
    return ','.join(map(lambda n: '"%s"' % n, get_ladder_players(ladder)))


def get_ranking_change(match):
    configuration = get_config(match.ladder,
        'leaderboard.swap_range',
        'leaderboard.advancement_distance',
        'leaderboard.auto_take_first'
    )
    if not match.ranking_change:
        return
    ranking_change_set = MatchRankingChangeSet.objects.create(ladder=match.ladder, change_date=timezone.now(), match=match)

def apply_ranking_change(ranking_change):
    pass

def adjust_rankings(match):
    SWAP_RANGE = get_config(match.ladder, 'leaderboard.swap_range')
    ADVANCEMENT_RANKS = get_config(match.ladder, 'leaderboard.advancement_distance')
    AUTO_TAKE_FIRST = get_config(match.ladder, 'leaderboard.auto_take_first')
    if not match.ranking_change:
        return

    winner = Ranked.objects.get(ladder=match.ladder, rank=Player.objects.get(user=match.winner().user, ladder=match.ladder).rank)
    loser = Ranked.objects.get(ladder=match.ladder, rank=Player.objects.get(user=match.loser().user, ladder=match.ladder).rank)
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
