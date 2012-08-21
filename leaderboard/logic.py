from django.utils import timezone

from core.models import Ranked, RankingChange
from core.logic import get_config
from leaderboard.models import Match, Player, MatchRankingChangeSet, MatchPlayer, GamePlayer

import logging
logger = logging.getLogger('monkeyladder')

def get_match_feed(ladder=None, order='-created', size=10):
    """
    Returns a match feed for the specified ladder
    """
    query = Match.objects.all()
    if ladder:
        query = query.filter(ladder=ladder)
    return query.order_by(order)[:size]

def get_players_match_feed(user, ladder=None, order='-match__created', size=10):
    """
    Returns a match feed for the specified ladder and user
    """
    query = MatchPlayer.objects.filter(user=user)
    if ladder:
        query = query.filter(match__ladder=ladder)
    return map(lambda p: p.match, query.order_by(order)[:size])

def count_players_wins(user, ladder=None):
    """
    Returns the users total matches won.

    If a ladder is supplied only that ladder will be considered
    """
    if ladder:
        return len(filter(lambda p: p.match.winner() == p, MatchPlayer.objects.filter(match__ladder=ladder, user=user)))
    return len(filter(lambda p: p.match.winner() == p, MatchPlayer.objects.filter(user=user)))

def count_players_losses(user, ladder=None):
    """
    Returns the users total matches lost.

    If a ladder is supplied only that ladder will be considered
    """
    if ladder:
        return len(filter(lambda p: p.match.loser() == p, MatchPlayer.objects.filter(match__ladder=ladder, user=user)))
    return len(filter(lambda p: p.match.loser() == p, MatchPlayer.objects.filter(user=user)))

def count_players_matches(user, ladder=None):
    """
    Returns the users total matches played.

    If a ladder is supplied only that ladder will be considered
    """
    return count_players_wins(user, ladder) + count_players_losses(user, ladder)

def calculate_players_match_win_percentage(user, ladder=None):
    wins = count_players_wins(user, ladder)
    matches = count_players_matches(user, ladder)
    if matches == 0:
        return 0
    return (float(wins) / float(matches)) * 100

def count_players_games(user, ladder=None):
    wins = 0
    games = 0
    if ladder:
        match_players = MatchPlayer.objects.filter(match__ladder=ladder, user=user)
    else:
        match_players = MatchPlayer.objects.filter(user=user)
    for match_player in match_players:
            if match_player.match.winner() == match_player:
                wins += match_player.score
            for other_match_player in match_player.match.matchplayer_set.all():
                games += other_match_player.score
    return wins, games

def calculate_players_game_win_percentage(user, ladder=None):
    wins, games = count_players_games(user, ladder)
    if games == 0:
        return 0
    return (float(wins) / float(games)) * 100

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
