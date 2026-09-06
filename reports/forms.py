from django import forms
from .models import WasteReport, WasteCategory


class WasteReportForm(forms.ModelForm):
    class Meta:
        model = WasteReport
        fields = ['title', 'category', 'location_name', 'estimated_weight_kg', 'urgency', 'image', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input', 
                'placeholder': 'e.g., Overflowing plastic bin near Food Court'
            }),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'location_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., North Wing Lawn, Hostel B Entrance'
            }),
            'estimated_weight_kg': forms.NumberInput(attrs={
                'class': 'form-input',
                'step': '0.5',
                'min': '0.1',
                'placeholder': 'Weight in kg (e.g. 2.5)'
            }),
            'urgency': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.FileInput(attrs={
                'class': 'form-file-input',
                'accept': 'image/*',
                'id': 'waste-photo-input'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 4,
                'placeholder': 'Describe what kind of waste, potential hazards, and any specific landmarks nearby...'
            }),
        }


class ReportVerificationForm(forms.ModelForm):
    award_points = forms.IntegerField(
        min_value=0,
        max_value=500,
        initial=30,
        widget=forms.NumberInput(attrs={'class': 'form-input'})
    )

    class Meta:
        model = WasteReport
        fields = ['status', 'verification_notes', 'cleaned_image']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'verification_notes': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 3,
                'placeholder': 'Enter staff notes, actions taken, or maintenance ticket IDs...'
            }),
            'cleaned_image': forms.FileInput(attrs={
                'class': 'form-file-input',
                'accept': 'image/*'
            }),
        }
