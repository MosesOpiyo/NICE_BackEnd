# Generated by Django 4.0 on 2023-11-20 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Notifications', '0004_notification_seen'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recipient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recepient_index', models.CharField(default='', max_length=10)),
            ],
        ),
        migrations.RemoveField(
            model_name='notification',
            name='recepient_index',
        ),
        migrations.AddField(
            model_name='notification',
            name='recipients',
            field=models.ManyToManyField(to='Notifications.Recipient'),
        ),
    ]