from matches.models import Match, MatchPlayer

import logging
logger = logging.getLogger('monkeyladder')

class MatchCreator(object):
    """
    Class to create a match for a ladder and associated records from player name, score tuples
    
    ie create(('player1', 2), ('player2', 3))
    """
    
    def __init__(self, ladder, *args, **kwargs):
        object.__init__(self, *args, **kwargs)
        self.ladder = ladder
        
    def create(self, *players):
        logger.debug("Creating a match with: {}".format(players))
        self._validate_scores(*map(lambda p: p[1], players))
        player_names = self._get_player_names(self.ladder)
        self._validate_players(player_names, *map(lambda p: p[0], players))
        self._create_match(self.ladder, players, player_names)
    
    def _validate_scores(self, *scores):
        logger.debug("Validating scores: {}".format(scores))
        try:
            for score in scores:
                if int(score) < 0:
                    logger.error("A score was negative")
                    raise AssertionError("Scores must be positive integers")
        except:
            logger.error("A score was incorrect")
            raise AssertionError("Scores must be positive integers")
        
    def _validate_players(self, player_names, *players):
        logger.debug("Validating players: {}".format(players))
        for player in players:
            if players.count(player) != 1:
                logger.error("Match has the same player more than once")
                raise AssertionError("Players must be unique")
            if player not in player_names:
                logger.error("A player was not on the ladder")
                raise AssertionError("Players must be on the ladder")
    
    def _get_player_names(self, ladder):
        player_names = {}
        for player in ladder.ranking():
            player_names[player.name()] = player.user
        return player_names
    
    def _create_match(self, ladder, players, player_names):
        match = Match(ladder=ladder)
        match.save()
        for player in players:
            match_player = MatchPlayer(match=match, user=player_names[player[0]], score=player[1])
            match_player.save()
            logger.debug("Created a match player: {}".format(match_player))
        logger.debug("Created a match: {}".format(match))
    
class RankingAlgorithm(object):
    
    def __init__(self, *args, **kwargs):
        object.__init__(self, *args, **kwargs)
    
    def adjust_rankings(self, match):
        pass