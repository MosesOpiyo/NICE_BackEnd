# Generated by Django 4.0 on 2023-10-18 14:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Farming', '0010_rename_producer_email_coffeeproducts_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coffeeproducts',
            name='email',
        ),
    ]
