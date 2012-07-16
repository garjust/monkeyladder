from django.contrib.auth.models import User
from django.db import models

from datedmodels.models import DatedModel

LADDER_TYPES = (
    ('BASIC', 'Basic'),
    ('LEADERBOARD', 'Leaderboard')
)

LADDER_PERMISSION_TYPES = (
    ('ADMIN', 'Administrator'),
    ('MOD', 'Moderator'),
    ('NORM', 'Normal'),
)

class Ladder(DatedModel):
    name = models.CharField(max_length=50)
    rungs = models.IntegerField()
    is_private = models.BooleanField(default=False)

    TYPES = LADDER_TYPES
    type = models.CharField(max_length=50, choices=TYPES, default='BASIC', editable=False)

    def ranking(self):
        return self.ranked_set.filter().order_by('rank')
    
    def watcher(self, user):
        if user.is_authenticated():
            return self.watcher_set.get(user=user)

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
        return str(self.rank)

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
        return self.ladderpermission.type == 'ADMIN'
    admin.boolean = True

    def mod(self):
        return self.ladderpermission.type == 'MOD'
    mod.boolean = True
    
    def norm(self):
        return self.ladderpermission.type == 'NORM'
    norm.boolean = True

    def __unicode__(self):
        return self.user.get_profile().name()
    
    class Meta:
        unique_together = ('ladder', 'user')

class LadderPermission(DatedModel):
    watcher = models.OneToOneField(Watcher)

    TYPES = LADDER_PERMISSION_TYPES
    type = models.CharField(max_length=50, choices=TYPES, default='NORM')

def create_ladder_permission(sender, instance, created, **kwargs):
    if created:
        LadderPermission.objects.create(watcher=instance)
models.signals.post_save.connect(create_ladder_permission, sender=Watcher)