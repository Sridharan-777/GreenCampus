from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('student', 'Student Eco-Champion'),
        ('marshal', 'Green Marshal / Staff'),
        ('admin', 'Sustainability Officer'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    department = models.CharField(max_length=100, blank=True, default='General Campus')
    hostel_or_block = models.CharField(max_length=100, blank=True, default='Main Block')
    eco_points = models.PositiveIntegerField(default=50)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(blank=True, default="Passionate about zero waste and a cleaner green campus.")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()}) - {self.eco_points} pts"

    @property
    def level(self):
        if self.eco_points >= 500:
            return "Eco Legend (Level 4)"
        elif self.eco_points >= 250:
            return "Waste Warrior (Level 3)"
        elif self.eco_points >= 100:
            return "Green Scout (Level 2)"
        return "Eco Novice (Level 1)"


class EcoBadge(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, default='fa-leaf')  # FontAwesome class name
    points_required = models.PositiveIntegerField(default=50)
    badge_color = models.CharField(max_length=30, default='#10b981')

    def __str__(self):
        return f"{self.name} ({self.points_required} pts)"


class UserBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='badges')
    badge = models.ForeignKey(EcoBadge, on_delete=models.CASCADE)
    awarded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'badge')

    def __str__(self):
        return f"{self.user.username} - {self.badge.name}"


class PointActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='point_activities')
    title = models.CharField(max_length=150)
    points = models.IntegerField(help_text="Positive for earned, negative for redeemed")
    activity_type = models.CharField(max_length=50, default='general')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} | {self.title} ({self.points:+d} pts)"


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()
