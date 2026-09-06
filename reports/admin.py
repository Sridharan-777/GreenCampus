from django.contrib import admin
from .models import WasteCategory, WasteReport

@admin.register(WasteCategory)
class WasteCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'base_eco_points', 'co2_saved_per_kg', 'badge_color')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(WasteReport)
class WasteReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'reported_by', 'category', 'location_name', 'status', 'urgency', 'points_awarded', 'created_at')
    list_filter = ('status', 'urgency', 'category')
    search_fields = ('title', 'location_name', 'reported_by__username', 'description')
