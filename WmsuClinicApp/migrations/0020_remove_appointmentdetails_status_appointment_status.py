# Generated by Django 5.0.1 on 2024-02-03 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WmsuClinicApp', '0019_remove_appointmentdetails_current_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointmentdetails',
            name='status',
        ),
        migrations.AddField(
            model_name='appointment',
            name='status',
            field=models.CharField(default='Pending', max_length=20),
        ),
    ]
