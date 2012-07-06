from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User
from core.models import Ladder, Player

class Match(models.Model):
    ladder = models.ForeignKey(Ladder)
    match_date = models.DateTimeField(default=timezone.now())

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
        
class Comment(models.Model):
    match = models.ForeignKey(Match)
    comment = models.CharField(max_length=100)
    creater = models.ForeignKey(User)
    created = models.DateTimeField(default=timezone.now())
    
    def __unicode__(self):
        return self.comment

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