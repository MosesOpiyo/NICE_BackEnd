# Generated by Django 4.0 on 2023-10-18 14:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Farming', '0012_coffeeproducts_farmer_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coffeeproducts',
            name='farmer_email',
        ),
    ]
