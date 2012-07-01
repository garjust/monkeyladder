from django.contrib import admin
from matches.models import Comment, Match, MatchPlayer

class PlayerInline(admin.TabularInline):
    model = MatchPlayer
    extra = 0
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1

class MatchAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['ladder', 'match_date']})
    ]
    inlines = [PlayerInline, CommentInline]
    list_display = ('__unicode__', 'ladder', 'match_date')
    list_filter = ['ladder', 'match_date']
    date_hierarchy = 'match_date'
    
    def has_add_permission(self, request):
        return False

admin.site.register(Match, MatchAdmin)
