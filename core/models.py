from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone

from django.contrib.auth.models import User

LADDER_TYPES = (
    ('BASIC', 'Basic'),
    ('LEADERBOARD', 'Leaderboard')
)

class DatedModel(models.Model):
    created = models.DateTimeField()
    created_by = models.ForeignKey(User, null=True, related_name='%(app_label)s_%(class)s_creator')
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        super(DatedModel, self).save(*args, **kwargs)
        
    class Meta:
        abstract = True

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
    
    TYPES = LADDER_TYPES
    type = models.CharField(max_length=50, choices=TYPES, default='BASIC', editable=False)

    def __unicode__(self):
        return str(self.rank)
        
class Favorite(DatedModel):
    ladder = models.ForeignKey(Ladder)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.ladder

class Watcher(DatedModel):
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