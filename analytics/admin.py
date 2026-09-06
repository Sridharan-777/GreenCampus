from django.contrib import admin
from .models import RewardItem, RewardRedemption

@admin.register(RewardItem)
class RewardItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'points_cost', 'available_stock', 'sponsor', 'is_active')

@admin.register(RewardRedemption)
class RewardRedemptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'reward', 'points_spent', 'redemption_code', 'is_claimed', 'created_at')
    list_filter = ('is_claimed',)
