from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

from datedmodels.models import DatedModel

LADDER_TYPES = (
    ('BASIC', 'Basic'),
    ('LEADERBOARD', 'Leaderboard')
)

LADDER_PERMISSION_TYPES = (
    ('ADMIN', 'Administrator'),
    ('MOD', 'Moderator'),
)

class Ladder(DatedModel):
    name = models.CharField(max_length=50)
    rungs = models.IntegerField()
    is_private = models.BooleanField(default=False)

    TYPES = LADDER_TYPES
    type = models.CharField(max_length=50, choices=TYPES, default='BASIC', editable=False)

    def ranking(self):
        return self.ranked_set.filter().order_by('rank')

    #@models.permalink
    def get_absolute_url(self):
        #return ('view_ladder', (), {'ladder_id': self.id})
        return '/ladders/{}/'.format(self.id)

    def __unicode__(self):
        return self.name

class Ranked(DatedModel):
    ladder = models.ForeignKey(Ladder)
    rank = models.IntegerField()
    info = models.CharField(max_length=50, null=True)

    TYPES = LADDER_TYPES
    type = models.CharField(max_length=50, choices=TYPES, default='BASIC', editable=False)

    def __unicode__(self):
        return str(self.info)
    
    class Meta:
        unique_together = ('ladder', 'rank')

class Favorite(DatedModel):
    ladder = models.ForeignKey(Ladder)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.ladder.name
    
    class Meta:
        unique_together = ('ladder', 'user')

class Watcher(DatedModel):
    ladder = models.ForeignKey(Ladder)
    user = models.ForeignKey(User)

    def admin(self):
        return self.ladderpermission_set.get(type='ADMIN')

    def mod(self):
        return self.ladderpermission_set.get(type='MOD')

    def __unicode__(self):
        return self.user.get_profile().name()
    
    class Meta:
        unique_together = ('ladder', 'user')

class LadderPermission(DatedModel):
    ladder = models.ForeignKey(Ladder)
    watcher = models.ForeignKey(Watcher)

    TYPES = LADDER_PERMISSION_TYPES
    type = models.CharField(max_length=50, choices=TYPES)
    
    class Meta:
        unique_together = ('ladder', 'watcher')

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    description = models.CharField(max_length=500, null=True, blank=True)

    def name(self):
        full_name = self.user.get_full_name()
        if full_name:
            return full_name
        return self.user.username
    
    @models.permalink
    def get_absolute_url(self):
        return ('view_profile', (), {'user_id': self.user.id})

    def __unicode__(self):
        return "{}'s Profile".format(self.name())

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
post_save.connect(create_user_profile, sender=User)
