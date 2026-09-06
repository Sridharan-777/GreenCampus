from django import forms
from django.contrib.auth.models import User
from .models import UserProfile


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Create a password (min 6 chars)'})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Confirm your password'})
    )
    role = forms.ChoiceField(
        choices=UserProfile.ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    department = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Computer Science, Mechanical'})
    )
    hostel_or_block = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Hostel A, Academic Block 2'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Choose username'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'your.name@campus.edu'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Last name'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password')
        p2 = cleaned_data.get('confirm_password')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data


class UserProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )
    last_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-input'})
    )

    class Meta:
        model = UserProfile
        fields = ['department', 'hostel_or_block', 'bio', 'avatar']
        widgets = {
            'department': forms.TextInput(attrs={'class': 'form-input'}),
            'hostel_or_block': forms.TextInput(attrs={'class': 'form-input'}),
            'bio': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
            'avatar': forms.FileInput(attrs={'class': 'form-file-input'}),
        }
