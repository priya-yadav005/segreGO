

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Household',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flat_number', models.CharField(max_length=20, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='household', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['flat_number'],
            },
        ),
        migrations.CreateModel(
            name='WasteEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('waste_type', models.CharField(choices=[('wet', 'Wet'), ('dry', 'Dry'), ('mixed', 'Mixed')], max_length=10)),
                ('date', models.DateField(auto_now_add=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('household', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='waste_entries', to='waste.household')),
            ],
            options={
                'verbose_name_plural': 'Waste Entries',
                'ordering': ['-date'],
            },
        ),
    ]
