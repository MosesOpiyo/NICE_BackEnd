# Generated by Django 4.0 on 2023-10-02 12:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Warehouser', '0005_shippingmanifest'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shippingmanifest',
            old_name='approved',
            new_name='shipping_approval',
        ),
    ]