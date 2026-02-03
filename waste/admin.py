from django.contrib import admin
from .models import Household, WasteEntry

@admin.register(Household)
class HouseholdAdmin(admin.ModelAdmin):
    list_display = ['flat_number', 'user', 'points', 'consecutive_days', 'tier', 'created_at']
    search_fields = ['flat_number', 'user__username']
    readonly_fields = ['points', 'consecutive_days', 'last_submission_date']

@admin.register(WasteEntry)
class WasteEntryAdmin(admin.ModelAdmin):
    list_display = ['household', 'waste_type', 'date']
    list_filter = ['waste_type', 'date']
    search_fields = ['household__flat_number']
    date_hierarchy = 'date'
