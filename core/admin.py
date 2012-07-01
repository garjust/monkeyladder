from core.models import Ladder, Player, Watcher#, Match, MatchPlayer
from django.contrib import admin

class PlayerInline(admin.TabularInline):
    model = Player
    extra = 1

class WatcherInline(admin.TabularInline):
    model = Watcher
    extra = 1

class LadderAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'rungs', 'is_private']}),
    ]
    inlines = [PlayerInline, WatcherInline]
    list_display = ('name', 'rungs', 'is_private', 'created')
    list_filter = ['is_private', 'created']
    search_fields = ['name']
    date_hierarchy = 'created'

#class MatchAdmin(admin.ModelAdmin):
#    fieldsets = [
#        (None, {'fields': ['ladder', 'match_date']})
#    ]
#    list_display = ('__unicode__', 'ladder', 'match_date')
#    list_filter = ['ladder', 'match_date']
#    date_hierarchy = 'match_date'
#    
#    def has_add_permission(self, request):
#        return False
#
#admin.site.register(Ladder, LadderAdmin)
#admin.site.register(Match, MatchAdmin)
