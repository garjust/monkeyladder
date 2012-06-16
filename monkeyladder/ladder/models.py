from django.db import models
from django.contrib.auth.models import User

class Ladder(models.Model):
    name = models.CharField(max_length=50)
    created = models.DateTimeField()
    rungs = models.IntegerField()
    #is_private = models.BooleanField()

    def __unicode__(self):
        return self.name

class LadderUser(models.Model):
    ladder = models.ForeignKey(Ladder)
    user = models.ForeignKey(User)
    rank = models.IntegerField()

    def __unicode__(self):
        return self.user.get_full_name()
