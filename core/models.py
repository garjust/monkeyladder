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
    description = models.CharField(max_length=50)

    def __unicode__(self):
        return str(self.description)

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

    TYPES = LADDER_PERMISSION_TYPES
    type = models.CharField(max_length=50, choices=TYPES, default='NORM')

    def admin(self):
        return self.type == 'ADMIN'
    admin.boolean = True

    def mod(self):
        return self.type == 'MOD'
    mod.boolean = True

    def norm(self):
        return self.type == 'NORM'
    norm.boolean = True

    def __unicode__(self):
        return self.user.get_profile().name()

    class Meta:
        unique_together = ('ladder', 'user')

class RankingChangeSet(DatedModel):
    ladder = models.ForeignKey(Ladder)
    change_date = models.DateTimeField()

    def __unicode__(self):
        return "%s ranking change on %s" % (self.ladder, self.change_date)

    class Meta:
        db_table = 'core_ranking_change_set'

class RankingChange(DatedModel):
    ranking_change_set = models.ForeignKey(RankingChangeSet)
    ranked = models.ForeignKey(Ranked)
    rank = models.PositiveIntegerField()
    change = models.IntegerField()

    def __unicode__(self):
        return "%s moved %s rank(s)" % (self.ranked, self.change)

    class Meta:
        db_table = 'core_ranking_change'
