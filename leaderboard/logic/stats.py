from leaderboard.models import MatchPlayer

import logging
logger = logging.getLogger('monkeyladder')

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
