from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone

class Ladder(models.Model):
    name = models.CharField(max_length=50)
    rungs = models.IntegerField()
    is_private = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now())

    def __unicode__(self):
        return self.name

class LadderUser(models.Model):
    ladder = models.ForeignKey(Ladder)
    user = models.ForeignKey(User)
    rank = models.IntegerField()

    def __unicode__(self):
        return self.user.get_full_name()

class LadderWatcher(models.Model):
    ladder = models.ForeignKey(Ladder)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.user.get_full_name()
