from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count, Q, Avg
from django.db.models import F
from .models import Household, WasteEntry, DailyReminder
from .forms import RegistrationForm, WasteEntryForm

def is_admin(user):

    return user.is_staff

def home(request):

    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin_dashboard')
        return redirect('submit_waste')
    return redirect('login')

def register(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            flat_number = form.cleaned_data.get('flat_number')
            Household.objects.create(user=user, flat_number=flat_number)
            messages.success(request, f'Account created for flat {flat_number}! Please log in.')
            return redirect('login')
    else:
        form = RegistrationForm()

    return render(request, 'waste/register.html', {'form': form})

@login_required
def submit_waste(request):

    if request.user.is_staff:
        return redirect('admin_dashboard')

    try:
        household = request.user.household
    except Household.DoesNotExist:
        messages.error(request, 'No household associated with your account.')
        return redirect('home')

    if request.method == 'POST':
        form = WasteEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.household = household
            entry.save()

            earned, bonus = household.award_points(entry.waste_type)

            household.calculate_segregation_score()

            household.update_daily_reminder()
            if bonus:
                messages.success(request, f'Waste entry submitted! You earned {earned} points (+{bonus} bonus). Total: {household.points} points. Streak: {household.consecutive_days} days.')
            else:
                messages.success(request, f'Waste entry submitted! You earned {earned} points. Total: {household.points} points. Streak: {household.consecutive_days} days.')
            return redirect('history')
    else:
        form = WasteEntryForm()

    return render(request, 'waste/submit_waste.html', {
        'form': form,
        'household': household
    })

@login_required
def leaderboard(request):

    households = Household.objects.order_by('-points', '-consecutive_days')[:50]

    for household in households:
        household.calculate_segregation_score()
    return render(request, 'waste/leaderboard.html', {'households': households})

@login_required
def history(request):

    if request.user.is_staff:
        return redirect('admin_dashboard')

    try:
        household = request.user.household

        household.calculate_segregation_score()
        entries = WasteEntry.objects.filter(household=household)

        from django.utils import timezone
        today_reminder = DailyReminder.objects.filter(
            household=household,
            date=timezone.localdate()
        ).first()
    except Household.DoesNotExist:
        entries = []
        household = None
        today_reminder = None

    return render(request, 'waste/history.html', {
        'entries': entries,
        'household': household,
        'today_reminder': today_reminder
    })

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):

    households = Household.objects.all()

    for household in households:
        household.calculate_segregation_score()

    recent_entries = WasteEntry.objects.select_related('household').order_by('-date')[:50]

    mixed_violators = Household.objects.annotate(
        mixed_count=Count('waste_entries', filter=Q(waste_entries__waste_type='mixed'))
    ).filter(mixed_count__gte=3).order_by('-mixed_count')

    total_entries = WasteEntry.objects.count()
    wet_count = WasteEntry.objects.filter(waste_type='wet').count()
    dry_count = WasteEntry.objects.filter(waste_type='dry').count()
    mixed_count = WasteEntry.objects.filter(waste_type='mixed').count()

    avg_segregation_score = Household.objects.aggregate(
        avg=Avg('area_segregation_score')
    )['avg'] or 0.0

    return render(request, 'waste/admin_dashboard.html', {
        'households': households,
        'recent_entries': recent_entries,
        'mixed_violators': mixed_violators,
        'total_entries': total_entries,
        'wet_count': wet_count,
        'dry_count': dry_count,
        'mixed_count': mixed_count,
        'avg_segregation_score': round(avg_segregation_score, 2),
    })
