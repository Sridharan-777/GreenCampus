from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


class CampaignCategory(models.Model):
    name = models.CharField(max_length=60, unique=True)
    slug = models.SlugField(max_length=60, unique=True)
    icon = models.CharField(max_length=50, default='fa-bullhorn')
    color = models.CharField(max_length=30, default='#3b82f6')

    class Meta:
        verbose_name_plural = 'Campaign Categories'

    def __str__(self):
        return self.name


class Campaign(models.Model):
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming Event'),
        ('ongoing', 'Ongoing Now'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    title = models.CharField(max_length=200, help_text="e.g., Campus Mega Clean-up & Plastic Drive 2026")
    category = models.ForeignKey(CampaignCategory, on_delete=models.SET_NULL, null=True, related_name='campaigns')
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_campaigns')
    description = models.TextField(help_text="Provide full details, mission, required gear, and meeting points.")
    
    banner_image = models.ImageField(upload_to='events/%Y/%m/', null=True, blank=True, help_text="Promotional event banner")
    location = models.CharField(max_length=200, help_text="e.g. North Lawn & Student Amphitheater")
    
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    
    target_volunteers = models.PositiveIntegerField(default=30)
    eco_points_reward = models.PositiveIntegerField(default=60, help_text="Eco-Points awarded upon verified attendance")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['start_date']

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

    def get_absolute_url(self):
        return reverse('event_detail', kwargs={'pk': self.pk})

    @property
    def rsvp_count(self):
        return self.rsvps.filter(status='registered').count()

    @property
    def progress_percentage(self):
        if self.target_volunteers > 0:
            pct = int((self.rsvp_count / self.target_volunteers) * 100)
            return min(pct, 100)
        return 0

    @property
    def is_past(self):
        return self.end_date < timezone.now()


class EventRSVP(models.Model):
    STATUS_CHOICES = [
        ('registered', 'Registered / Confirmed'),
        ('attended', 'Attended (Points Awarded)'),
        ('cancelled', 'Cancelled'),
    ]

    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='rsvps')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rsvps')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='registered')
    volunteer_role = models.CharField(max_length=100, blank=True, default='Volunteer')
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('campaign', 'user')

    def __str__(self):
        return f"{self.user.username} -> {self.campaign.title} ({self.status})"
