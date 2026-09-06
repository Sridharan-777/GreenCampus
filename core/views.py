from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserRegisterForm, UserProfileUpdateForm
from .models import UserProfile, EcoBadge, UserBadge, PointActivity


def home(request):
    """Modern interactive landing page with campus sustainability overview."""
    top_champions = UserProfile.objects.select_related('user').order_by('-eco_points')[:5]
    badges = EcoBadge.objects.all()[:4]
    
    # Check if reports and events models exist to display highlights
    recent_reports = []
    upcoming_events = []
    
    try:
        from reports.models import WasteReport
        recent_reports = WasteReport.objects.select_related('reported_by').order_by('-created_at')[:4]
    except Exception:
        pass

    try:
        from events.models import Campaign
        upcoming_events = Campaign.objects.filter(is_active=True).order_by('start_date')[:3]
    except Exception:
        pass

    context = {
        'top_champions': top_champions,
        'badges': badges,
        'recent_reports': recent_reports,
        'upcoming_events': upcoming_events,
    }
    return render(request, 'core/home.html', context)


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Update UserProfile
            profile = user.profile
            profile.role = form.cleaned_data.get('role', 'student')
            profile.department = form.cleaned_data.get('department', '')
            profile.hostel_or_block = form.cleaned_data.get('hostel_or_block', '')
            profile.eco_points = 50  # Welcome signup bonus
            profile.save()

            # Record point activity
            PointActivity.objects.create(
                user=user,
                title="Welcome Eco-Bonus",
                points=50,
                activity_type="signup"
            )

            login(request, user)
            messages.success(request, f"Welcome to GreenCampus, {user.username}! You received 50 Eco-Points as a welcome bonus 🌱")
            return redirect('dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserRegisterForm()

    return render(request, 'core/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            next_url = request.GET.get('next', 'dashboard')
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'core/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out successfully. Keep conserving resources!")
    return redirect('home')


@login_required
def profile_view(request, username=None):
    if username:
        user_obj = get_object_or_404(User, username=username)
    else:
        user_obj = request.user

    is_own_profile = (request.user == user_obj)
    profile = user_obj.profile
    activities = user_obj.point_activities.all()[:10]
    user_badges = user_obj.badges.select_related('badge').all()

    # User's reports
    user_reports = user_obj.reports.all().order_by('-created_at')[:5] if hasattr(user_obj, 'reports') else []
    
    # User's RSVPs
    user_rsvps = user_obj.rsvps.select_related('campaign').all().order_by('-registered_at')[:5] if hasattr(user_obj, 'rsvps') else []

    if request.method == 'POST' and is_own_profile:
        form = UserProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            user_obj.first_name = form.cleaned_data.get('first_name')
            user_obj.last_name = form.cleaned_data.get('last_name')
            user_obj.email = form.cleaned_data.get('email')
            user_obj.save()
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
    else:
        initial_data = {
            'first_name': user_obj.first_name,
            'last_name': user_obj.last_name,
            'email': user_obj.email,
        }
        form = UserProfileUpdateForm(instance=profile, initial=initial_data)

    context = {
        'profile_user': user_obj,
        'profile': profile,
        'is_own_profile': is_own_profile,
        'form': form,
        'activities': activities,
        'user_badges': user_badges,
        'user_reports': user_reports,
        'user_rsvps': user_rsvps,
    }
    return render(request, 'core/profile.html', context)
