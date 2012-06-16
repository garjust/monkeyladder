from ladders.models import *
from django.contrib import admin

class LadderUserInline(admin.TabularInline):
    model = LadderUser
    extra = 1

class LadderAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'rungs', 'is_private']}),
    ]
    inlines = [LadderUserInline]
    list_display = ('name', 'rungs', 'is_private', 'created')
    list_filter = ['is_private', 'created']
    search_fields = ['name']
    date_hierarchy = 'created'

admin.site.register(Ladder, LadderAdmin)
