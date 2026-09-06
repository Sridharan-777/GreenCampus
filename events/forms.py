from django import forms
from .models import Campaign, EventRSVP


class CampaignForm(forms.ModelForm):
    start_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'form-input', 'type': 'datetime-local'})
    )
    end_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'form-input', 'type': 'datetime-local'})
    )

    class Meta:
        model = Campaign
        fields = ['title', 'category', 'location', 'start_date', 'end_date', 'target_volunteers', 'eco_points_reward', 'banner_image', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g., Campus Mega Clean-up & Plastic Drive 2026'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'location': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g., Central Quadrangle & North Lawn'}),
            'target_volunteers': forms.NumberInput(attrs={'class': 'form-input', 'min': '1', 'placeholder': 'Target number of participants'}),
            'eco_points_reward': forms.NumberInput(attrs={'class': 'form-input', 'min': '10', 'placeholder': 'Points rewarded upon participation'}),
            'banner_image': forms.FileInput(attrs={'class': 'form-file-input', 'accept': 'image/*'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 5, 'placeholder': 'Detailed agenda, required apparel/gloves, gathering point...'}),
        }


class EventRSVPForm(forms.ModelForm):
    class Meta:
        model = EventRSVP
        fields = ['volunteer_role']
        widgets = {
            'volunteer_role': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Trash Sorter, Logistics, Registration Desk'}),
        }
