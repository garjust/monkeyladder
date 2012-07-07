from core.models import Ladder, Ranked, Watcher
from django.contrib import admin

class RankedInline(admin.TabularInline):
    model = Ranked
    extra = 1

class WatcherInline(admin.TabularInline):
    model = Watcher
    extra = 1

class LadderAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'rungs', 'is_private']}),
    ]
    inlines = [RankedInline, WatcherInline]
    list_display = ('name', 'rungs', 'is_private', 'created')
    list_filter = ['is_private', 'created']
    search_fields = ['name']
    date_hierarchy = 'created'

admin.site.register(Ladder, LadderAdmin)
