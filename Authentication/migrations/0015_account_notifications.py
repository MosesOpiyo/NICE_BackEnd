# Generated by Django 4.0 on 2023-11-25 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Notifications', '0006_remove_notification_recipients_delete_recipient'),
        ('Authentication', '0014_alter_profile_profile_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='notifications',
            field=models.ManyToManyField(to='Notifications.Notification'),
        ),
    ]