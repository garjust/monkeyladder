from django.db import models

from django.contrib.auth.models import User
from core.models import Ladder, Ranked, LADDER_TYPES
from datedmodels.models import DatedModel

class Player(Ranked):
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.user.get_profile().name()
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.type = LADDER_TYPES['LEADERBOARD']
        super(Player, self).save(*args, **kwargs)

class Match(DatedModel):
    ladder = models.ForeignKey(Ladder)
    winner = models.ForeignKey(User, related_name='%(app_label)s_%(class)s_won_match')
    winner_score = models.PositiveIntegerField()
    loser = models.ForeignKey(User, related_name='%(app_label)s_%(class)s_lost_match')
    loser_score = models.PositiveIntegerField()
    ranking_change = models.BooleanField()

    def __unicode__(self):
        return "{} ({}) vs {} ({})".format(self.winner.get_profile().name(), self.winner_score, self.loser.get_profile().name(), self.loser_score)
    
    class Meta:
        verbose_name_plural = "Matches"
    
class Game(DatedModel):
    match = models.ForeignKey(Match)
    winner_score = models.PositiveIntegerField(null=True)
    loser_score = models.PositiveIntegerField(null=True)
    
    def __unicode__(self):
        return "{} ({}) vs {} ({}) Game".format(self.match.winner, self.winner_score, self.match.loser, self.loser_score)