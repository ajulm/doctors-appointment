# Generated by Django 4.1.3 on 2024-07-23 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_appointment_is_active_appointment_scheduled_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='customer_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
