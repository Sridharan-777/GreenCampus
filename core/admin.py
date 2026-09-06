from django.contrib import admin
from .models import UserProfile, EcoBadge, UserBadge, PointActivity

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'department', 'hostel_or_block', 'eco_points', 'created_at')
    list_filter = ('role', 'department')
    search_fields = ('user__username', 'user__email', 'department')

@admin.register(EcoBadge)
class EcoBadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'points_required', 'icon', 'badge_color')

@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ('user', 'badge', 'awarded_at')

@admin.register(PointActivity)
class PointActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'points', 'activity_type', 'created_at')
    list_filter = ('activity_type',)
