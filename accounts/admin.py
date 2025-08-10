from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Follow


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_verified', 'created_at']
    list_filter = ['is_verified', 'is_staff', 'is_active', 'created_at']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-created_at']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Profile Info', {
            'fields': ('bio', 'profile_picture', 'date_of_birth', 'location', 'website', 'is_verified')
        }),
    )


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['follower', 'following', 'created_at']
    list_filter = ['created_at']
    search_fields = ['follower__username', 'following__username']
    ordering = ['-created_at']


admin.site.register(User, CustomUserAdmin)
