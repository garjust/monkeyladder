from django.contrib.auth.models import User
from django.db import models

from datedmodels.models import DatedModel

LADDER_TYPES = (
    ('BASIC', 'Basic'),
    ('LEADERBOARD', 'Leaderboard')
)

LADDER_CONFIGURATION_TYPES = (
    ('STR', 'String'),
    ('INT', 'Integer'),
    ('BOOL', 'Boolean'),
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

    def is_leaderboard(self):
        return self.type == 'LEADERBOARD'

    def watcher_count(self):
        return self.watcher_set.count()

    def favorite_count(self):
        return self.watcher_set.filter(favorite=True).count()

    #@models.permalink
    def get_absolute_url(self):
        #return ('view_ladder', (), {'ladder_id': self.id})
        return '/ladders/{}/'.format(self.id)

    def __unicode__(self):
        return self.name

class LadderConfigurationKey(DatedModel):
    key = models.CharField(max_length=50)

    TYPES = LADDER_CONFIGURATION_TYPES
    type = models.CharField(max_length=50, choices=TYPES)

    def __unicode__(self):
        return self.key

    class Meta:
        db_table = 'core_ladder_configuration_key'

class LadderConfiguration(DatedModel):
    ladder = models.ForeignKey(Ladder, null=True)
    key = models.ForeignKey(LadderConfigurationKey)
    raw_value = models.CharField(max_length=300)

    def type(self):
        return self.key.type

    def value(self):
        try:
            return {
                'STR': str,
                'INT': int,
                'BOOL': lambda raw: bool(int(raw))
            }[self.type()](self.raw_value)
        except ValueError:
            pass

    def __unicode__(self):
        return '%s=%s' % (self.key, self.value())

    class Meta:
        unique_together = ('ladder', 'key')
        db_table = 'core_ladder_configuration'

class Ranked(DatedModel):
    ladder = models.ForeignKey(Ladder)
    rank = models.IntegerField()
    description = models.CharField(max_length=50)

    def display(self):
        try:
            return self.player.display()
        except:
            return self.__unicode__()

    def __unicode__(self):
        return self.description

class Watcher(DatedModel):
    ladder = models.ForeignKey(Ladder)
    user = models.ForeignKey(User)
    favorite = models.BooleanField(default=False)

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
        return "%s ranking change on %s" % (self.ladder, self.change_date.strftime('%Y-%m-%d %H:%M:%S'))

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
