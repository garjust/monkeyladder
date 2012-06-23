from django.db import models
from django.utils import timezone

import django.contrib.auth.models as djangoauth

class Ladder(models.Model):
    name = models.CharField(max_length=50)
    rungs = models.IntegerField()
    is_private = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now())

    def ranking(self):
        return self.player_set.filter().order_by('rank')

    def matches(self, order='-match_date'):
        return self.match_set.filter().order_by(order)

    def __unicode__(self):
        return self.name

class Player(models.Model):
    ladder = models.ForeignKey(Ladder)
    user = models.ForeignKey(djangoauth.User)
    rank = models.IntegerField()

    def __unicode__(self):
        return self.user.get_full_name()

class Watcher(models.Model):
    ladder = models.ForeignKey(Ladder)
    user = models.ForeignKey(djangoauth.User)

    def __unicode__(self):
        return self.user.get_full_name()

class Match(models.Model):
    ladder = models.ForeignKey(Ladder)
    match_date = models.DateTimeField(default=timezone.now())

    def winner(self):
        return self.matchplayer_set.filter().order_by('score')[0]
    def loser(self):
        return self.matchplayer_set.filter().order_by('score')[1]

    def __unicode__(self):
        return "{} Match".format(self.ladder.name, self.winner(), self.loser())

class MatchPlayer(models.Model):
    match = models.ForeignKey(Match)
    player = models.ForeignKey(Player)
    score = models.IntegerField()

    def __unicode__(self):
        return "{} ({})".format(self.player, self.score)