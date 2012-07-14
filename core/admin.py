from django.contrib import admin

from core.models import Ladder, Ranked, Watcher, Favorite

class RankedInline(admin.TabularInline):
    model = Ranked
    extra = 1
    fieldsets = [
        (None, {'fields': ['rank', 'info']}),
    ]

class WatcherInline(admin.TabularInline):
    model = Watcher
    extra = 0
    fieldsets = [
        (None, {'fields': ['user']}),
    ]

class FavoriteInline(admin.TabularInline):
    model = Favorite
    extra = 0
    fieldsets = [
        (None, {'fields': ['user']}),
    ]

class LadderAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'rungs', 'is_private']}),
    ]
    inlines = [RankedInline, WatcherInline, FavoriteInline]
    list_display = ('name', 'type', 'rungs', 'is_private', 'created')
    list_filter = ['is_private', 'created']
    search_fields = ['name']
    date_hierarchy = 'created'

admin.site.register(Ladder, LadderAdmin)
