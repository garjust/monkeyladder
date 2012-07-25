from django.contrib import admin

from core.models import Ladder, LadderConfiguration, Ranked, Watcher, RankingChangeSet, RankingChange

class RankedInline(admin.TabularInline):
    model = Ranked
    extra = 1
    fieldsets = [
        (None, {'fields': ['rank', 'description']}),
    ]

class WatcherInline(admin.TabularInline):
    model = Watcher
    extra = 0
    fieldsets = [
        (None, {'fields': ['user']}),
    ]

class LadderConfigurationInline(admin.TabularInline):
    model = LadderConfiguration
    extra = 0
    fieldsets = [
        (None, {'fields': ['key', 'raw_value']}),
    ]

class LadderAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'rungs', 'is_private']}),
        ('Meta', {'fields': ['created', 'created_by']})
    ]
    inlines = [RankedInline, LadderConfigurationInline, WatcherInline]
    list_display = ('name', 'type', 'rungs', 'is_private', 'created')
    list_filter = ['is_private', 'created']
    search_fields = ['name']
    date_hierarchy = 'created'

class WatcherAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['user', 'ladder', 'favorite', 'type']}),
    ]
    list_display = ('user', 'ladder', 'created', 'type', 'favorite')
    list_filter = ['ladder', 'created', 'favorite']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'ladder__name']
    date_hierarchy = 'created'

class RankingChangeInline(admin.TabularInline):
    model = RankingChange
    extra = 0

class RankingChangeSetAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['ladder', 'change_date']})
    ]
    inlines = [RankingChangeInline]
    list_display = ('ladder', 'change_date')
    list_filter = ['ladder', 'change_date']
    search_fields = ['ladder', 'change_data']
    date_hierarchy = 'change_date'

class LadderConfigurationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['ladder', 'key', 'raw_value']})
    ]
    list_display = ('ladder', 'key', 'value', 'type')
    list_filter = ['key', 'ladder', 'key__type']
    search_fields = ['key', 'ladder__name', 'ladder__type', 'value']
    date_hierarchy = 'created'

admin.site.register(Ladder, LadderAdmin)
admin.site.register(LadderConfiguration, LadderConfigurationAdmin)
admin.site.register(Watcher, WatcherAdmin)
admin.site.register(RankingChangeSet, RankingChangeSetAdmin)
