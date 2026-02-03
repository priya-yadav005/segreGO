
from django.db import migrations, models
import django.utils.timezone

class Migration(migrations.Migration):

    dependencies = [
        ('waste', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='household',
            name='points',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='household',
            name='consecutive_days',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='household',
            name='last_submission_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
