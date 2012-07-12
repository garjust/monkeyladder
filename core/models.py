from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

from datedmodels.models import DatedModel

LADDER_TYPES = (
    ('BASIC', 'Basic'),
    ('LEADERBOARD', 'Leaderboard')
)

class Ladder(DatedModel):
    name = models.CharField(max_length=50)
    rungs = models.IntegerField()
    is_private = models.BooleanField(default=False)

    TYPES = LADDER_TYPES
    type = models.CharField(max_length=50, choices=TYPES, default='BASIC', editable=False)

    def ranking(self):
        return self.ranked_set.filter().order_by('rank')

    @models.permalink
    def get_absolute_url(self):
        return ('core.views.ladder', (), {
            'ladder_id': self.id
        })

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

class Favorite(DatedModel):
    ladder = models.ForeignKey(Ladder)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.ladder.name

class Watcher(DatedModel):
    ladder = models.ForeignKey(Ladder)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.user.get_profile().name()

    class Meta:
        permissions = (
            ('edit_ranks', "Can edit the ranking of the watchers ladder"),
        )

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    description = models.CharField(max_length=500, null=True, blank=True)

    def name(self):
        full_name = self.user.get_full_name()
        if full_name:
            return full_name
        return self.user.username

    def __unicode__(self):
        return "{}'s Profile".format(self.name())

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
post_save.connect(create_user_profile, sender=User)
