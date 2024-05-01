# Generated by Django 5.0.1 on 2024-01-31 22:35

import WmsuClinicApp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WmsuClinicApp', '0010_profile_remove_appointment_student_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('admin_username', models.CharField(max_length=50, unique=True)),
                ('admin_password', models.CharField(max_length=50)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('middle_name', models.CharField(blank=True, max_length=30, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='profile',
            name='User_type',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='id_number',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='position',
        ),
        migrations.AddField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='facebook_links',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='instagram_links',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='profilepictures.jpg', upload_to=WmsuClinicApp.models.user_profile_picture_path),
        ),
        migrations.AddField(
            model_name='profile',
            name='status',
            field=models.CharField(default='Active', max_length=10),
        ),
    ]