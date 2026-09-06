from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class WasteCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='fa-trash-alt')
    badge_color = models.CharField(max_length=30, default='#10b981')
    base_eco_points = models.PositiveIntegerField(default=20, help_text="Points awarded when verified")
    co2_saved_per_kg = models.DecimalField(max_digits=5, decimal_places=2, default=1.50, help_text="kg of CO2 avoided per kg of waste recycled")

    class Meta:
        verbose_name_plural = 'Waste Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class WasteReport(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('in_progress', 'Clean-up In Progress'),
        ('cleaned', 'Cleaned & Resolved'),
        ('rejected', 'Rejected / Invalid'),
    ]

    URGENCY_CHOICES = [
        ('low', 'Low (Non-urgent)'),
        ('medium', 'Medium (Standard)'),
        ('high', 'High (Overflowing / Hazard)'),
        ('critical', 'Critical (Immediate Attention)'),
    ]

    title = models.CharField(max_length=150, help_text="Brief summary, e.g. Overflowing plastic bins near Library")
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    category = models.ForeignKey(WasteCategory, on_delete=models.SET_NULL, null=True, related_name='reports')
    location_name = models.CharField(max_length=150, help_text="e.g. Science Block 2 Entrance, Hostel C Backside")
    description = models.TextField(blank=True, help_text="Provide context on waste type and severity")
    
    # Image upload
    image = models.ImageField(upload_to='reports/%Y/%m/', help_text="Photo evidence of waste condition")
    
    # Clean-up resolution photo
    cleaned_image = models.ImageField(upload_to='resolutions/%Y/%m/', null=True, blank=True, help_text="Photo evidence after cleaning")
    
    estimated_weight_kg = models.DecimalField(max_digits=6, decimal_places=2, default=2.00, help_text="Estimated waste weight in kilograms")
    urgency = models.CharField(max_length=20, choices=URGENCY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    points_awarded = models.PositiveIntegerField(default=0)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_reports')
    verification_notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.get_status_display()}] {self.title} by {self.reported_by.username}"

    def get_absolute_url(self):
        return reverse('report_detail', kwargs={'pk': self.pk})

    @property
    def estimated_co2_saved(self):
        if self.category and self.status == 'cleaned':
            return round(float(self.estimated_weight_kg) * float(self.category.co2_saved_per_kg), 2)
        return 0.0
