from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Campaign, CampaignCategory, EventRSVP
from .forms import CampaignForm, EventRSVPForm
from core.models import PointActivity


@login_required
def event_list(request):
    """Member 2: Campaign & Event Management listing view (Requires Login)."""
    status_filter = request.GET.get('status', 'upcoming')
    category_slug = request.GET.get('category')
    search_query = request.GET.get('q')

    events = Campaign.objects.filter(is_active=True).select_related('organizer', 'category').prefetch_related('rsvps')

    if status_filter and status_filter != 'all':
        events = events.filter(status=status_filter)
    
    if category_slug:
        events = events.filter(category__slug=category_slug)
        
    if search_query:
        events = events.filter(
            Q(title__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    categories = CampaignCategory.objects.all()

    context = {
        'events': events,
        'categories': categories,
        'selected_status': status_filter,
        'selected_category': category_slug,
        'search_query': search_query,
    }
    return render(request, 'events/event_list.html', context)


@login_required
def event_detail(request, pk):
    event = get_object_or_404(Campaign.objects.select_related('organizer', 'category').prefetch_related('rsvps__user'), pk=pk)
    
    user_rsvp = None
    is_registered = False
    if request.user.is_authenticated:
        user_rsvp = EventRSVP.objects.filter(campaign=event, user=request.user).first()
        is_registered = bool(user_rsvp and user_rsvp.status == 'registered')

    # RSVPs list
    active_rsvps = event.rsvps.filter(status__in=['registered', 'attended']).select_related('user__profile')
    is_organizer = (request.user.is_authenticated and (request.user == event.organizer or request.user.is_staff))

    context = {
        'event': event,
        'user_rsvp': user_rsvp,
        'is_registered': is_registered,
        'active_rsvps': active_rsvps,
        'is_organizer': is_organizer,
    }
    return render(request, 'events/event_detail.html', context)


@login_required
def event_create(request):
    if request.method == 'POST':
        form = CampaignForm(request.POST, request.FILES)
        if form.is_valid():
            campaign = form.save(commit=False)
            campaign.organizer = request.user
            campaign.save()

            messages.success(request, f"Sustainability Campaign '{campaign.title}' created successfully! 🎉")
            return redirect('event_detail', pk=campaign.pk)
        else:
            messages.error(request, "Please check the form for errors.")
    else:
        form = CampaignForm()

    return render(request, 'events/event_form.html', {'form': form})


@login_required
def event_rsvp_toggle(request, pk):
    event = get_object_or_404(Campaign, pk=pk)

    if request.method == 'POST':
        rsvp, created = EventRSVP.objects.get_or_create(campaign=event, user=request.user)

        if not created and rsvp.status == 'registered':
            # Cancel RSVP
            rsvp.status = 'cancelled'
            rsvp.save()
            messages.info(request, f"You have cancelled your RSVP for '{event.title}'.")
        else:
            rsvp.status = 'registered'
            rsvp.volunteer_role = request.POST.get('volunteer_role', 'Volunteer')
            rsvp.save()
            messages.success(request, f"You're in! 🎉 You registered for '{event.title}'. Earn +{event.eco_points_reward} points upon participation.")

    return redirect('event_detail', pk=pk)


@login_required
def event_confirm_attendance(request, pk, user_id):
    """Organizer or staff marks volunteer attendance and awards eco points."""
    event = get_object_or_404(Campaign, pk=pk)

    if not (request.user == event.organizer or request.user.is_staff or getattr(request.user.profile, 'role', '') in ['marshal', 'admin']):
        messages.error(request, "Unauthorized to verify event attendance.")
        return redirect('event_detail', pk=pk)

    rsvp = get_object_or_404(EventRSVP, campaign=event, user_id=user_id)

    if rsvp.status != 'attended':
        rsvp.status = 'attended'
        rsvp.save()

        # Award points to attendee
        user_profile = rsvp.user.profile
        user_profile.eco_points += event.eco_points_reward
        user_profile.save()

        PointActivity.objects.create(
            user=rsvp.user,
            title=f"Volunteered at: {event.title[:35]}",
            points=event.eco_points_reward,
            activity_type="event_attended"
        )
        messages.success(request, f"Attendance confirmed for {rsvp.user.username}! +{event.eco_points_reward} Eco-Points awarded.")
    else:
        messages.info(request, f"Attendance already confirmed for {rsvp.user.username}.")

    return redirect('event_detail', pk=pk)
