# Generated by Django 4.0 on 2023-09-18 13:09

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0004_profile_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=cloudinary.models.CloudinaryField(max_length=255, null=True, verbose_name='images/'),
        ),
    ]
