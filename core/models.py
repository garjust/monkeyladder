from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone

from django.contrib.auth.models import User

class Ladder(models.Model):
    name = models.CharField(max_length=50)
    rungs = models.IntegerField()
    is_private = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now())
    created_by = models.ForeignKey(User)

    def ranking(self):
        return self.player_set.filter().order_by('rank')

    def match_feed(self, order='-match_date', size=5):
        return self.match_set.filter().order_by(order)[:size]

    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        super(Ladder, self).save(*args, **kwargs)

class Player(models.Model):
    ladder = models.ForeignKey(Ladder)
    user = models.ForeignKey(User)
    rank = models.IntegerField()

    def __unicode__(self):
        return self.user.get_profile().name()

class Watcher(models.Model):
    ladder = models.ForeignKey(Ladder)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.user.get_full_name()
    
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    paddle = models.CharField(max_length=300, null=True, blank=True)
    
    def name(self):
        full_name = self.user.get_full_name()
        if full_name:
            return full_name
        return self.user.username
    
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
post_save.connect(create_user_profile, sender=User)