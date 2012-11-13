from accounts.models import UserProfile
from django.contrib import admin


class UserProfileAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['user', 'about']}),
    ]
    list_display = ['user', 'name']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
admin.site.register(UserProfile, UserProfileAdmin)
