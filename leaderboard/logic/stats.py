from leaderboard.models import MatchPlayer

import logging
logger = logging.getLogger('monkeyladder')


def get_stats(user, ladder=None, other_user_id=None):
    """
    Returns a package of a users various statistics

    Includes: matches won, matches played, games won, games player, match win %, game win %
    """
    def calculate_win_percentage(wins, played):
        if not played:
            return float(0)
        return (float(wins) / float(played)) * 100
    matches_won, matches_played = get_match_stats(user, ladder, other_user_id)
    games_won, games_played = get_game_stats(user, ladder, other_user_id)
    return {
        'matches_won': matches_won,
        'matches_played': matches_played,
        'match_win_percentage': calculate_win_percentage(matches_won, matches_played),
        'games_won': games_won,
        'games_played': games_played,
        'game_win_percentage': calculate_win_percentage(games_won, games_played),
    }


def get_match_stats(user, ladder=None, other_user_id=None):
    wins = 0
    games = 0
    match_players = MatchPlayer.objects.filter(user=user)
    if ladder:
        match_players = match_players.filter(match__ladder=ladder)
    for match_player in match_players:
        if other_user_id and other_user_id not in [other_match_player.user.id for other_match_player in match_player.match.matchplayer_set.all()]:
            continue
        if match_player.match.winner() == match_player:
            wins += 1
        games += 1
    return wins, games


def get_game_stats(user, ladder=None, other_user_id=None):
    wins = 0
    games = 0
    match_players = MatchPlayer.objects.filter(user=user)
    if ladder:
        match_players = match_players.filter(match__ladder=ladder)
    for match_player in match_players:
            if other_user_id and other_user_id not in [other_match_player.user.id for other_match_player in match_player.match.matchplayer_set.all()]:
                continue
            wins += match_player.score
            for a_match_player in match_player.match.matchplayer_set.all():
                games += a_match_player.score
    return wins, games
