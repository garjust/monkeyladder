from django.contrib import admin

from accounts.models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['user', 'about']}),
    ]
    
admin.site.register(UserProfile, UserProfileAdmin)

