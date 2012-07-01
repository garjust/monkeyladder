from core.models import Ladder, Player, Watcher
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

admin.site.register(Ladder, LadderAdmin)
