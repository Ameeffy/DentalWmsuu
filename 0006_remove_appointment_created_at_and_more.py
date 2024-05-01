# Generated by Django 5.0.1 on 2024-01-31 19:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WmsuClinicApp', '0005_alter_appointment_facultystaff_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='reference_number',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='status',
        ),
        migrations.CreateModel(
            name='AppointmentDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, default='pending', max_length=20)),
                ('reference_number', models.CharField(blank=True, max_length=50, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('appointment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WmsuClinicApp.appointment')),
            ],
        ),
    ]