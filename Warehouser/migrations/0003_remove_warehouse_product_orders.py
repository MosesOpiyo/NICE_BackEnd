# Generated by Django 4.0 on 2023-10-02 10:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Warehouser', '0002_alter_productorder_buyer_alter_productorder_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='warehouse',
            name='product_orders',
        ),
    ]