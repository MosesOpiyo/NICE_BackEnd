# Generated by Django 4.0 on 2023-09-25 11:46

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0010_alter_profile_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=cloudinary.models.CloudinaryField(default='https://res.cloudinary.com/dlzyg12i7/image/upload/v1695058480/user_dy7js1.jpg', max_length=255, verbose_name='images'),
        ),
    ]
