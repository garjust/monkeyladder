from django.contrib import admin

from core.models import Ladder, Ranked, Watcher, Favorite, RankingChangeSet, RankingChange

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

class FavoriteAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['user', 'ladder']}),
    ]
    list_display = ('user', 'ladder', 'created')
    list_filter = ['created']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'ladder__name']
    date_hierarchy = 'created'

class WatcherAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['user', 'ladder', 'type']}),
    ]
    list_display = ('user', 'ladder', 'created', 'type')
    list_filter = ['ladder', 'created']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'ladder__name']
    date_hierarchy = 'created'

class RankingChangeInline(admin.TabularInline):
    model = RankingChange

class RankingChangeSetAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['ladder', 'change_date']})
    ]
    inlines = [RankingChangeInline]

admin.site.register(Ladder, LadderAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Watcher, WatcherAdmin)
admin.site.register(RankingChangeSet, RankingChangeSetAdmin)
