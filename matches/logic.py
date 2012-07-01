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
            if player not in player_names:
                logger.error("A player was not on the ladder")
                raise AssertionError("Players must be on the ladder")
    
    def _get_player_names(self, ladder):
        player_names = {}
        for player in ladder.ranking():
            player_names[player.user.get_full_name()] = player.user
        return player_names
    
    def _create_match(self, ladder, players, player_names):
        match = Match(ladder=ladder)
        match.save()
        for player in players:
            match_player = MatchPlayer(match=match, user=player_names[player[0]], score=player[1])
            match_player.save()
            logger.debug("Created a match player: {}".format(match_player))
        logger.debug("Created a match: {}".format(match))
    
    def _adjust_rankings(self, players, winner, loser):
        rank_diff = winner.rank - loser.rank
        if rank_diff <= 0:
            return
        elif rank_diff <= 2:
            temp = winner.rank
            winner.rank = loser.rank
            loser.rank = temp
            winner.save()
            loser.save()
        else:
            players_slice = players[loser.rank-1:winner.rank]
            players_slice[0].rank += 1
            players_slice[1].rank -= 1
            players_slice[len(players_slice)-1].rank -= 2
            players_slice[len(players_slice)-2].rank += 1
            players_slice[len(players_slice)-3].rank += 1
            for player in players_slice:
                player.save()