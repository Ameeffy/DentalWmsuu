# Generated by Django 5.0.1 on 2024-02-03 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WmsuClinicApp', '0015_remove_appointment_appointment_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointmentdetails',
            name='details_text',
        ),
        migrations.AddField(
            model_name='appointmentdetails',
            name='status',
            field=models.CharField(default='Pending', max_length=20),
        ),
    ]
