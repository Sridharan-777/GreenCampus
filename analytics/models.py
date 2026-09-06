from django.db import models
from django.contrib.auth.models import User


class RewardItem(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    points_cost = models.PositiveIntegerField(default=100)
    icon = models.CharField(max_length=50, default='fa-gift')
    image = models.ImageField(upload_to='rewards/', null=True, blank=True)
    available_stock = models.PositiveIntegerField(default=50)
    sponsor = models.CharField(max_length=100, default='Campus Sustainability Office')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} ({self.points_cost} pts)"


class RewardRedemption(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='redemptions')
    reward = models.ForeignKey(RewardItem, on_delete=models.CASCADE, related_name='redemptions')
    points_spent = models.PositiveIntegerField()
    redemption_code = models.CharField(max_length=20, unique=True)
    is_claimed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} redeemed {self.reward.title} ({self.redemption_code})"
