# Generated by Django 4.0 on 2023-12-15 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0020_alter_verificationcode_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='phone_number',
            field=models.TextField(default=''),
        ),
    ]
