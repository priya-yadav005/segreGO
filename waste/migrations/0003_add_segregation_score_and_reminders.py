

from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('waste', '0002_add_rewards'),
    ]

    operations = [
        migrations.AddField(
            model_name='household',
            name='area_segregation_score',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='household',
            name='daily_reminder_enabled',
            field=models.BooleanField(default=True),
        ),
        migrations.CreateModel(
            name='DailyReminder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('message', models.CharField(max_length=255)),
                ('is_sent', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('household', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='daily_reminders', to='waste.household')),
            ],
            options={
                'ordering': ['-date'],
                'unique_together': {('household', 'date')},
            },
        ),
    ]
