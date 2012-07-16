from django.contrib import admin
from leaderboard.models import Match, Game, Player

class GameInline(admin.TabularInline):
    model = Game
    extra = 0
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False

class MatchAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['ladder', 'created']})
    ]
    inlines = [GameInline]
    list_display = ('__unicode__', 'ladder', 'created')
    list_filter = ['ladder', 'created']
    date_hierarchy = 'created'
    
    def has_add_permission(self, request):
        return False
    
class PlayerAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['ladder', 'rank', 'user']})
    ]
    list_display = ('user', 'ladder', 'rank', 'created')
    list_filter = ['user', 'created']
    date_hierarchy = 'created'

admin.site.register(Match, MatchAdmin)
admin.site.register(Player, PlayerAdmin)
