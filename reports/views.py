from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import WasteReport, WasteCategory
from .forms import WasteReportForm, ReportVerificationForm
from core.models import PointActivity


@login_required
def report_list(request):
    """View all campus waste reports with category and status filters (Requires Login)."""
    category_slug = request.GET.get('category')
    status_filter = request.GET.get('status')
    search_query = request.GET.get('q')

    reports = WasteReport.objects.select_related('reported_by', 'category').all()

    if category_slug:
        reports = reports.filter(category__slug=category_slug)
    if status_filter:
        reports = reports.filter(status=status_filter)
    if search_query:
        reports = reports.filter(
            Q(title__icontains=search_query) |
            Q(location_name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    categories = WasteCategory.objects.all()

    # Summary counts
    total_count = WasteReport.objects.count()
    cleaned_count = WasteReport.objects.filter(status='cleaned').count()
    pending_count = WasteReport.objects.filter(status='pending').count()

    context = {
        'reports': reports,
        'categories': categories,
        'selected_category': category_slug,
        'selected_status': status_filter,
        'search_query': search_query,
        'total_count': total_count,
        'cleaned_count': cleaned_count,
        'pending_count': pending_count,
    }
    return render(request, 'reports/report_list.html', context)


@login_required
def report_detail(request, pk):
    report = get_object_or_404(WasteReport.objects.select_related('reported_by', 'category', 'verified_by'), pk=pk)
    
    # Check if logged in user has permission to verify
    can_verify = False
    if request.user.is_authenticated:
        if request.user.is_staff or getattr(request.user.profile, 'role', '') in ['marshal', 'admin']:
            can_verify = True

    verification_form = None
    if can_verify:
        verification_form = ReportVerificationForm(instance=report, initial={'award_points': report.category.base_eco_points if report.category else 25})

    context = {
        'report': report,
        'can_verify': can_verify,
        'verification_form': verification_form,
    }
    return render(request, 'reports/report_detail.html', context)


@login_required
def report_create(request):
    """Member 1: Waste report submission with image upload & category selection."""
    if request.method == 'POST':
        form = WasteReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.reported_by = request.user
            report.save()

            messages.success(request, "Waste report submitted successfully! Green Marshals have been notified 🌿")
            return redirect('report_detail', pk=report.pk)
        else:
            messages.error(request, "Please ensure all required fields (including photo) are filled properly.")
    else:
        form = WasteReportForm()

    categories = WasteCategory.objects.all()
    return render(request, 'reports/report_form.html', {'form': form, 'categories': categories})


@login_required
def report_verify(request, pk):
    """Action for Green Marshals or Admins to verify/resolve a waste report and award points."""
    report = get_object_or_404(WasteReport, pk=pk)
    
    if not (request.user.is_staff or getattr(request.user.profile, 'role', '') in ['marshal', 'admin']):
        messages.error(request, "Only Green Marshals or Campus Staff can verify reports.")
        return redirect('report_detail', pk=pk)

    if request.method == 'POST':
        form = ReportVerificationForm(request.POST, request.FILES, instance=report)
        if form.is_valid():
            new_status = form.cleaned_data['status']
            award_points = form.cleaned_data.get('award_points', 0)

            report.verified_by = request.user
            
            # If changed to cleaned/resolved and points not yet awarded
            if new_status == 'cleaned' and report.points_awarded == 0 and award_points > 0:
                report.points_awarded = award_points
                # Update reporter's profile points
                reporter_profile = report.reported_by.profile
                reporter_profile.eco_points += award_points
                reporter_profile.save()

                # Add point log
                PointActivity.objects.create(
                    user=report.reported_by,
                    title=f"Report Resolved: {report.title[:30]}",
                    points=award_points,
                    activity_type="waste_report_verified"
                )
                messages.success(request, f"Report marked as Cleaned! {award_points} Eco-Points awarded to @{report.reported_by.username}.")
            else:
                messages.success(request, f"Report status updated to '{report.get_status_display()}'.")

            form.save()
            return redirect('report_detail', pk=report.pk)

    return redirect('report_detail', pk=pk)


@login_required
def my_reports(request):
    reports = WasteReport.objects.filter(reported_by=request.user).order_by('-created_at')
    return render(request, 'reports/my_reports.html', {'reports': reports})
