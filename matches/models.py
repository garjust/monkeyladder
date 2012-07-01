from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User
from core.models import Ladder

class Match(models.Model):
    ladder = models.ForeignKey(Ladder)
    summary = models.CharField(max_length=300, null=True, blank=True)
    match_date = models.DateTimeField(default=timezone.now())

    def winner(self):
        return self.matchplayer_set.filter().order_by('score')[1]
    def loser(self):
        return self.matchplayer_set.filter().order_by('score')[0]

    def __unicode__(self):
        return "{} vs {}".format(self.winner(), self.loser())
    
    class Meta:
        verbose_name_plural = "Matches"

class MatchPlayer(models.Model):
    match = models.ForeignKey(Match)
    user = models.ForeignKey(User)
    score = models.IntegerField()

    def __unicode__(self):
        return "{} ({})".format(self.user, self.score)