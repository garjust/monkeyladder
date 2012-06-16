from ladder.models import *
from django.contrib import admin

class LadderUserInline(admin.TabularInline):
    model = LadderUser
    extra = 1

class LadderAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'rungs']}),
        ('Other', {'fields': ['created'], 'classes': ['collapse']})
    ]
    inlines = [LadderUserInline]
    list_display = ('name', 'rungs', 'created')

admin.site.register(Ladder, LadderAdmin)
