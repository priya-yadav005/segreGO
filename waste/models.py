from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Household(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='household')
    flat_number = models.CharField(max_length=20, unique=True)

    points = models.IntegerField(default=0)
    consecutive_days = models.IntegerField(default=0)
    last_submission_date = models.DateField(blank=True, null=True)

    area_segregation_score = models.FloatField(default=0.0)
    daily_reminder_enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Flat {self.flat_number}"

    class Meta:
        ordering = ['flat_number']

    def award_points(self, waste_type):

        today = timezone.localdate()

        if waste_type == 'mixed':
            earned = 2
        else:
            earned = 10

        bonus = 0
        if self.last_submission_date:

            if (today - self.last_submission_date) == timedelta(days=1):
                self.consecutive_days += 1
            elif (today - self.last_submission_date) > timedelta(days=1):

                self.consecutive_days = 1
            else:

                pass
        else:
            self.consecutive_days = 1

        if self.consecutive_days and self.consecutive_days % 7 == 0:
            bonus = 50

        total_gain = earned + bonus
        self.points = (self.points or 0) + total_gain
        self.last_submission_date = today
        self.save(update_fields=['points', 'consecutive_days', 'last_submission_date'])
        return earned, bonus

    @property
    def tier(self):

        if self.points >= 1000:
            return 'Platinum'
        if self.points >= 500:
            return 'Gold'
        if self.points >= 200:
            return 'Silver'
        return 'Bronze'

    def calculate_segregation_score(self):

        entries = self.waste_entries.all()
        if not entries.exists():
            return 0.0

        properly_segregated = entries.filter(waste_type__in=['wet', 'dry']).count()
        total = entries.count()

        score = (properly_segregated / total * 100) if total > 0 else 0.0
        self.area_segregation_score = round(score, 2)
        self.save(update_fields=['area_segregation_score'])
        return self.area_segregation_score

    def update_daily_reminder(self):

        today = timezone.localdate()

        reminder, created = DailyReminder.objects.get_or_create(
            household=self,
            date=today,
            defaults={'message': self.get_default_reminder_message()}
        )
        return reminder

    def get_default_reminder_message(self):

        score = self.calculate_segregation_score()

        if score >= 90:
            return "🌟 Excellent! Keep up your great segregation practices!"
        elif score >= 75:
            return "👍 Good job! Your segregation score is improving."
        elif score >= 50:
            return "📝 Remember to segregate wet and dry waste properly."
        else:
            return "⚠️ Please pay more attention to waste segregation."

class DailyReminder(models.Model):

    household = models.ForeignKey(Household, on_delete=models.CASCADE, related_name='daily_reminders')
    date = models.DateField(auto_now_add=True)
    message = models.CharField(max_length=255)
    is_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.household.flat_number} - {self.date}"

    class Meta:
        ordering = ['-date']
        unique_together = ('household', 'date')

class WasteEntry(models.Model):

    WASTE_TYPE_CHOICES = [
        ('wet', 'Wet'),
        ('dry', 'Dry'),
        ('mixed', 'Mixed'),
    ]

    household = models.ForeignKey(Household, on_delete=models.CASCADE, related_name='waste_entries')
    waste_type = models.CharField(max_length=10, choices=WASTE_TYPE_CHOICES)
    date = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.household.flat_number} - {self.waste_type} - {self.date}"

    class Meta:
        ordering = ['-date']
        verbose_name_plural = "Waste Entries"
