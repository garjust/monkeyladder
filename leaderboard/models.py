from django.db import models

from django.contrib.auth.models import User
from core.models import Ladder, Ranked, RankingChangeSet
from datedmodels.models import DatedModel


class Player(Ranked):
    user = models.ForeignKey(User)

    def display(self):
        return self.__unicode__()

    def __unicode__(self):
        return self.user.get_profile().name()

    def save(self, *args, **kwargs):
        if not self.id:
            self.description = self.user.username
        super(Player, self).save(*args, **kwargs)


class Match(DatedModel):
    ladder = models.ForeignKey(Ladder)
    ranking_change = models.BooleanField()

    def games(self):
        return self.game_set.all()

    def winner(self):
        return reduce(lambda l, r: l if l.score > r.score else r, self.matchplayer_set.all())

    def loser(self):
        return reduce(lambda l, r: l if l.score <= r.score else r, self.matchplayer_set.all())

    #@models.permalink
    def get_absolute_url(self):
        return '%s/matches/?id=%s' % (self.ladder.get_absolute_url(), self.id)

    def __unicode__(self):
        return "{} ({}) vs {} ({})".format(self.winner().user.get_profile().name(), self.winner().score, self.loser().user.get_profile().name(), self.loser().score)

    class Meta:
        verbose_name_plural = "Matches"


class MatchPlayer(models.Model):
    match = models.ForeignKey(Match)
    user = models.ForeignKey(User)
    score = models.PositiveIntegerField()

    def __unicode__(self):
        return '%s match player' % self.user.username

    class Meta:
        db_table = 'leaderboard_match_player'
        unique_together = ('match', 'user')


class Game(DatedModel):
    match = models.ForeignKey(Match)
    game_number = models.PositiveIntegerField()

    def winner(self):
        return reduce(lambda l, r: l if l.score > r.score else r, self.gameplayer_set.all())

    def loser(self):
        return reduce(lambda l, r: l if l.score <= r.score else r, self.gameplayer_set.all())

    def __unicode__(self):
        return "{} ({}) {} ({})".format(self.winner().player.user.get_profile().name(), self.winner().score, self.loser().player.user.get_profile().name(), self.loser().score)

    class Meta:
        ordering = ['game_number']


class GamePlayer(models.Model):
    game = models.ForeignKey(Game)
    player = models.ForeignKey(MatchPlayer)
    score = models.PositiveIntegerField()

    def __unicode__(self):
        return '%s game player' % self.player.user.username

    class Meta:
        db_table = 'leaderboard_game_player'
        unique_together = ('game', 'player')


class MatchRankingChangeSet(RankingChangeSet):
    match = models.ForeignKey(Match)

    def __unicode__(self):
        return "%s (Match)" % super(MatchRankingChangeSet, self).__unicode__()

    class Meta:
        db_table = 'leaderboard_match_ranking_change_set'
