from django.contrib import admin
from .models import CampaignCategory, Campaign, EventRSVP

@admin.register(CampaignCategory)
class CampaignCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon', 'color')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('title', 'organizer', 'category', 'start_date', 'status', 'target_volunteers', 'eco_points_reward', 'is_active')
    list_filter = ('status', 'category', 'is_active')
    search_fields = ('title', 'location', 'description', 'organizer__username')

@admin.register(EventRSVP)
class EventRSVPAdmin(admin.ModelAdmin):
    list_display = ('user', 'campaign', 'status', 'volunteer_role', 'registered_at')
    list_filter = ('status',)
