from django.contrib import admin
from matches.models import Match, MatchPlayer

class PlayerInline(admin.TabularInline):
    model = MatchPlayer
    extra = 0
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False

class MatchAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['ladder', 'match_date']})
    ]
    inlines = [PlayerInline]
    list_display = ('__unicode__', 'ladder', 'match_date')
    list_filter = ['ladder', 'match_date']
    date_hierarchy = 'match_date'
    
    def has_add_permission(self, request):
        return False

admin.site.register(Match, MatchAdmin)
