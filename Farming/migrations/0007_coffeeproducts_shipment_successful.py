# Generated by Django 4.0 on 2023-09-25 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Farming', '0006_processedproducts_price_processedproducts_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='coffeeproducts',
            name='shipment_successful',
            field=models.BooleanField(default=False),
        ),
    ]