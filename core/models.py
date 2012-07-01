from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone

from django.contrib.auth.models import User

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
    user = models.ForeignKey(User)
    rank = models.IntegerField()

    def __unicode__(self):
        return self.user.get_full_name()

class Watcher(models.Model):
    ladder = models.ForeignKey(Ladder)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.user.get_full_name()
    
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    paddle = models.CharField(max_length=300, null=True, blank=True)
    
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
post_save.connect(create_user_profile, sender=User)