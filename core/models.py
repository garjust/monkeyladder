from django.contrib.auth.models import User
from django.db import models

from datedmodels.models import DatedModel
from ladder_types import LADDER_TYPES


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
    TYPES = LADDER_TYPES

    name = models.CharField(max_length=50)
    rungs = models.IntegerField()
    is_private = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    type = models.CharField(max_length=50, choices=TYPES, default='BASIC', editable=False)

    def ranking(self):
        return self.ranked_set.order_by('rank')

    def last_change(self):
        changes = self.rankingchangeset_set.order_by('-change_date')
        return changes[0] if changes else None

    def watcher(self, user):
        """DEPRECATED"""
        if user.is_authenticated():
            try:
                return self.watcher_set.get(user=user)
            except Watcher.DoesNotExist:
                pass

    def is_leaderboard(self):
        """DEPRECATED"""
        return self.type == 'LEADERBOARD'

    def watcher_count(self):
        """DEPRECATED"""
        return self.watcher_set.count()

    def favorite_count(self):
        """DEPRECATED"""
        return self.watcher_set.filter(favorite=True).count()

    #@models.permalink
    def get_absolute_url(self):
        #return ('view_ladder', (), {'ladder_id': self.id})
        return '/ladders/%s/%s' % (self.type.lower(), self.id)

    def get_general_url(self):
        return '/ladders/%s' % self.id

    def __unicode__(self):
        return self.name


class LadderConfigurationKey(DatedModel):
    key = models.CharField(max_length=50, unique=True)

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
