from django.contrib import admin
from leaderboard.models import Match, Game, Player, MatchRankingChangeSet

from ladders.admin import RankingChangeInline

class GameInline(admin.TabularInline):
    model = Game
    extra = 0

class MatchAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['ladder', 'created']})
    ]
    inlines = [GameInline]
    list_display = ('__unicode__', 'ladder', 'created')
    list_filter = ['ladder', 'created']
    date_hierarchy = 'created'

class PlayerAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['ladder', 'rank', 'description', 'user']})
    ]
    list_display = ('user', 'ladder', 'rank', 'created')
    list_filter = ['user', 'created']
    date_hierarchy = 'created'

class MatchRankingChangeSetAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['ladder', 'change_date', 'match']})
    ]
    inlines = [RankingChangeInline]
    list_display = ('match', 'ladder', 'change_date')
    list_filter = ['ladder', 'change_date']
    search_fields = ['ladder', 'change_data']
    date_hierarchy = 'change_date'

admin.site.register(Match, MatchAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(MatchRankingChangeSet, MatchRankingChangeSetAdmin)
