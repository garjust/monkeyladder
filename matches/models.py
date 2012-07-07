from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User
from core.models import Ladder, Ranked, LADDER_TYPES

class Player(Ranked):
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.user.get_profile().name()
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.type = LADDER_TYPES['LEADERBOARD']
        super(Player, self).save(*args, **kwargs)

class Match(models.Model):
    ladder = models.ForeignKey(Ladder)
    match_date = models.DateTimeField()

    def winner(self):
        return self.matchplayer_set.filter().order_by('score')[1]
    
    def loser(self):
        return self.matchplayer_set.filter().order_by('score')[0]
    
    def comments(self, order='-created'):
        return self.comment_set.filter().order_by(order) 

    def __unicode__(self):
        return "{} vs {}".format(self.winner(), self.loser())
    
    class Meta:
        verbose_name_plural = "Matches"
        
    def save(self, *args, **kwargs):
        if not self.id:
            self.match_date = timezone.now()
        super(Match, self).save(*args, **kwargs)

class MatchPlayer(models.Model):
    match = models.ForeignKey(Match)
    user = models.ForeignKey(User)
    score = models.IntegerField()
    
    def player(self):
        return Player.objects.filter(ladder=self.match.ladder, user=self.user)[0]

    def __unicode__(self):
        if self.user.get_full_name():
            return "{} ({})".format(self.user.get_full_name(), self.score)
        return "{} ({})".format(self.user.username, self.score)